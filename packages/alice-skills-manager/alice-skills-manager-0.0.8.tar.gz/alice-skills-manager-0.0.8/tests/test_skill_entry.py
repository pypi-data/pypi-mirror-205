import pytest
from os.path import exists, join, dirname, abspath

from asm import SkillEntry


class TestSkillEntry(object):
    def setup(self):
        self.root = dirname(abspath(__file__))
        self.url = 'https://github.com/testuser/testrepo.git/'
        self.entry = SkillEntry(
            'test-name', 'test-path',
            url='https://github.com/testuser/testrepo.git/'
        )

    def test_https_init(self):
        s = SkillEntry('test-name', 'test-path',
                       url='https://github.com/testuser/testrepo.git/')
        assert s.author == 'testuser'

    def test_git_ssl_init(self):
        s = SkillEntry('test-name', 'test-path',
                       url='git@github.com:forslund/skill-cocktail.git')
        assert s.author == ''

    def test_attach(self):
        """Attach a remote entry to a local entry"""
        remote = SkillEntry(
            'test-name2', 'test-path2',
            url='https://github.com/testname/testrepo2.git/'
        )
        self.entry.is_local = True
        self.entry.attach(remote)
        assert self.entry.url == remote.url
        assert self.entry.path == 'test-path'
        assert self.entry.is_local

    def test_from_folder(self):
        entry = SkillEntry.from_folder('test/folder')
        assert entry.name == 'folder'
        assert entry.url == ''

    def test_create_path(self):
        SkillEntry.create_path('myfolder', 'https://github.com/myname/myrepo')
        SkillEntry.create_path(
            'myfolder', 'https://github.com/myname/myrepo', 'skillname'
        )

    def test_extract_repo_name(self):
        assert SkillEntry.extract_repo_name(self.url) == 'testrepo'

    def test_extract_repo_id(self):
        assert SkillEntry.extract_repo_id(self.url) == 'testuser:testrepo'

    def test_match(self):
        assert self.entry.match('test-name') == 1.0
        assert self.entry.match('test-name', 'testuser') == 1.0
        assert self.entry.match('jsfaiasfa') < 0.5
        assert self.entry.match('test-name', 'fjasfa') < 1.0

    def test_run_pip(self):
        assert self.entry.run_pip() is False

    def test_run_requirements_sh(self):
        assert self.entry.run_requirements_sh() is False

    def test_run_skill_requirements(self):
        with pytest.raises(ValueError):
            self.entry.run_skill_requirements()

    def get_dependent_skills(self):
        reqs = join(self.path, "skill_requirements.txt")
        if not exists(reqs):
            return []

        with open(reqs, "r") as f:
            return [i.strip() for i in f.readlines() if i.strip()]

    def test_repr(self):
        str(self.entry)
