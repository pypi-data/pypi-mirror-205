from glob import glob
from os import makedirs
from os.path import exists, join, isdir, dirname, basename, normpath
import json
from tempfile import gettempdir

from xdg import BaseDirectory
from git import Repo
from git.exc import GitCommandError, GitError

from alice_skills_manager import git_to_asm_exceptions
from asm.exceptions import AsmException
from asm.util import cached_property, Git
import logging
import requests

LOG = logging.getLogger(__name__)

ALICE_SKILLS_DATA = ("https://raw.githubusercontent.com/"
                       "MycroftAI/mycroft-skills-data")
FIVE_MINUTES = 300


def download_skills_data(branch, path):
    """Download and if possible save skills meta-data as local cache.

    Arguments:
        branch: skills-repo branch to fetch data for
        path: path to skills meta-data cache.

    Returns:
        (dict) skills meta-data as dict.
    """
    market_info_url = (ALICE_SKILLS_DATA + "/" + branch +
                       "/skill-metadata.json")
    try:
        info = requests.get(market_info_url).json()
    except (requests.HTTPError, requests.exceptions.ConnectionError) as e:
        LOG.warning("Skill metadata couldn't be fetched "
                    "({})".format(repr(e)))
        info = {}
    if info:
        # Cache the received data
        try:
            with open(path, 'w') as f:
                json.dump(info, f)
        except Exception as e:
            LOG.warning('Couldn\'t save cached version of '
                        'skills-metadata.json ({})'.format(e))
    return info


def load_cached_skills_data(path):
    """Load cached skills_data from file.

    Arguments:
        path:   path of meta-data cache.

    Returns:
        (dict) skills meta-data as dict.
    """
    try:
        with open(path) as f:
            info = json.load(f)
    except Exception:
        LOG.warning('skills-metadata cache exists but can\'t '
                    'be parsed')
        info = {}
    return info


def load_skills_data(branch, path):
    """Load skills data, either from web or local cache.

    Arguments:
        branch: skills-repo branch to fetch data for
        path: path to skills meta-data cache.

    Returns:
        dict where key is a skill github repo and value is the meta-data entry
        for the skill.
    """
    info = download_skills_data(branch, path)

    # Try to load cache if fetching failed
    if not info and exists(path):
        info = load_cached_skills_data(path)

    # Return data indexed by repo
    return {info[k]['repo'].lower(): info[k] for k in info}


class SkillRepo(object):
    def __init__(self, url=None, branch=None):
        self.path = join(BaseDirectory.save_data_path('alice'),
                         'skills-repo')
        self.url = url or "https://github.com/Alice-IA/alice-skills"
        self.branch = branch or "21.02"
        self.repo_info = {}

    @cached_property(ttl=FIVE_MINUTES)
    def skills_meta_info(self):
        try:
            skills_meta_cache = normpath(join(self.path,
                                              '..', 'skills-meta.json'))
            skills_meta_info = load_skills_data(self.branch,
                                                skills_meta_cache)
        except Exception as e:
            LOG.exception(repr(e))
            skills_meta_info = {}

        return skills_meta_info

    def read_file(self, filename):
        with open(join(self.path, filename)) as f:
            return f.read()

    def __prepare_repo(self):
        if not exists(dirname(self.path)):
            makedirs(dirname(self.path))

        if not isdir(self.path):
            Repo.clone_from(self.url, self.path)

        git = Git(self.path)
        git.config('remote.origin.url', self.url)
        git.fetch()

        try:
            git.checkout(self.branch)
            git.reset('origin/' + self.branch, hard=True)
        except GitCommandError:
            raise AsmException('Invalid branch: ' + self.branch)

    def update(self):
        try:
            self.__prepare_repo()
        except (GitError, PermissionError) as e:
            LOG.warning('Could not prepare repo ({}), '
                        ' Creating temporary repo'.format(repr(e)))
            original_path = self.path
            self.path = join(gettempdir(), '.skills-repo')
            try:
                with git_to_asm_exceptions():
                    self.__prepare_repo()
            except Exception:
                LOG.warning('Could not use temporary repo either ({}), '
                            ' trying to use existing one without '
                            'update'.format(repr(e)))
                self.path = original_path  # Restore path to previous value
                raise

    def get_skill_data(self):
        """ generates tuples of name, path, url, sha """
        path_to_sha = {
            folder: sha for folder, sha in self.get_shas()
        }
        modules = self.read_file('.gitmodules').split('[submodule "')
        for i, module in enumerate(modules):
            if not module:
                continue
            try:
                name = module.split('"]')[0].strip()
                path = module.split('path = ')[1].split('\n')[0].strip()
                url = module.split('url = ')[1].strip()
                sha = path_to_sha.get(path, '')
                yield name, path, url, sha
            except (ValueError, IndexError) as e:
                LOG.warning('Failed to parse submodule "{}" #{}:{}'.format(
                    locals().get('name', ''), i, e
                ))

    def get_shas(self):
        git = Git(self.path)
        with git_to_asm_exceptions():
            shas = git.ls_tree('origin/' + self.branch)
        for line in shas.split('\n'):
            size, typ, sha, folder = line.split()
            if typ != 'commit':
                continue
            yield folder, sha

    def get_default_skill_names(self):
        for defaults_file in glob(join(self.path, 'DEFAULT-SKILLS*')):
            with open(defaults_file) as f:
                skills = list(filter(
                    lambda x: x and not x.startswith('#'),
                    map(str.strip, f.read().split('\n'))
                ))
            platform = basename(defaults_file).replace('DEFAULT-SKILLS', '')
            platform = platform.replace('.', '') or 'default'
            yield platform, skills
