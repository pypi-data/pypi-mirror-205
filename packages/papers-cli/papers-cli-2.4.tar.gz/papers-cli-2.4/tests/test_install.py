import os
import json
import shutil
import tempfile
import unittest
import subprocess as sp
from papers.config import Config
from papers.config import CONFIG_FILE
from papers.bib import Biblio
# from pathlib import Path

from tests.common import paperscmd, prepare_paper, run, PAPERSCMD, BaseTest as TestBaseInstall, LocalInstallTest, GlobalInstallTest

bibtex2 = """@article{SomeOneElse2000,
 author = {Some One},
 doi = {10.5194/xxxx},
 title = {Interesting Stuff},
 year = {2000}
}"""


class TestLocalInstall(TestBaseInstall):

    def test_install(self):
        self.assertFalse(self._exists(self.mybib))
        self.assertFalse(self._exists(self.filesdir))
        self.papers(f'install --force --local --bibtex {self.mybib} --files {self.filesdir}')
        # Config file was created:
        self.assertTrue(self._exists(".papers/config.json"))
        # Values of config file match input:
        config = Config.load(self._path(".papers/config.json"))
        self.assertEqual(config.bibtex, os.path.abspath(self._path(self.mybib)))
        self.assertEqual(config.filesdir, os.path.abspath(self._path(self.filesdir)))
        self.assertFalse(config.git)
        # bibtex and files directory were created:
        self.assertTrue(self._exists(self.mybib))
        self.assertTrue(self._exists(self.filesdir))


    def test_install_defaults_no_preexisting_bibtex(self):
        self.assertFalse(self._exists(self.mybib))
        self.assertFalse(self._exists(self.filesdir))
        self.assertFalse(self._exists(".papers/config.json"))
        # pre-existing bibtex?
        os.remove(self._path(self.anotherbib))
        self.assertFalse(self._exists(self.anotherbib))
        self.papers(f'install --force --local')
        self.assertTrue(self._exists(".papers/config.json"))
        config = Config.load(self._path(".papers/config.json"))
        # self.assertEqual(config.bibtex, os.path.abspath(self._path("papers.bib")))
        self.assertEqual(config.bibtex, os.path.abspath(self._path("papers.bib")))
        self.assertEqual(config.filesdir, os.path.abspath(self._path("files")))
        self.assertFalse(config.git)


    def test_install_defaults_preexisting_bibtex(self):
        self.assertFalse(self._exists(self.mybib))
        self.assertFalse(self._exists(self.filesdir))
        self.assertFalse(self._exists(".papers/config.json"))
        # pre-existing bibtex
        self.assertTrue(self._exists(self.anotherbib))
        self.assertFalse(self._exists("papers.bib"))
        self.papers(f'install --force --local')
        self.assertTrue(self._exists(".papers/config.json"))
        config = Config.load(self._path(".papers/config.json"))
        self.assertEqual(config.bibtex, os.path.abspath(self._path(self.anotherbib)))
        self.assertEqual(config.filesdir, os.path.abspath(self._path("files")))
        self.assertFalse(config.git)


    def test_install_defaults_preexisting_pdfs(self):
        self.assertFalse(self._exists(self.filesdir))
        self.assertFalse(self._exists(".papers/config.json"))
        # pre-existing pdfs folder (pre-defined set of names)
        os.makedirs(self._path("pdfs"))
        self.papers(f'install --force --local')
        self.assertTrue(self._exists(".papers/config.json"))
        config = Config.load(self._path(".papers/config.json"))
        # self.assertEqual(config.bibtex, os.path.abspath(self._path("papers.bib")))
        self.assertEqual(config.bibtex, os.path.abspath(self._path(self.anotherbib)))
        self.assertEqual(config.filesdir, os.path.abspath(self._path("pdfs")))
        self.assertFalse(config.git)

    def test_install_raise(self):
        self.papers(f'install --force --local --bibtex {self.mybib} --files {self.filesdir}')
        self.assertTrue(self._exists(".papers/config.json"))
        self.assertTrue(self._exists(self.mybib))
        self.assertTrue(self._exists(self.filesdir))
        f = lambda : self.papers(f'install --local --bibtex {self.mybib} --files {self.filesdir}')
        self.assertRaises(Exception, f)

    def test_install_force(self):
        self.papers(f'install --force --local --bibtex {self.mybib} --files {self.filesdir}')
        self.assertTrue(self._exists(".papers/config.json"))
        self.assertTrue(self._exists(self.mybib))
        self.assertTrue(self._exists(self.filesdir))
        config = Config.load(self._path(".papers/config.json"))
        self.assertEqual(config.bibtex, os.path.abspath(self._path(self.mybib)))
        self.assertEqual(config.filesdir, os.path.abspath(self._path(self.filesdir)))
        self.papers(f'install --local --force --bibtex {self.mybib}XX')
        config = Config.load(self._path(".papers/config.json"))
        self.assertEqual(config.bibtex, os.path.abspath(self._path(self.mybib + "XX")))
        # The files folder from previous install was forgotten
        self.assertEqual(config.filesdir, os.path.abspath(self._path("files")))
        self.assertFalse(config.git)

    def test_install_edit(self):
        self.papers(f'install --force --local --bibtex {self.mybib} --files {self.filesdir}')
        self.assertTrue(self._exists(".papers/config.json"))
        self.assertTrue(self._exists(self.mybib))
        self.assertTrue(self._exists(self.filesdir))
        config = Config.load(self._path(".papers/config.json"))
        self.assertEqual(config.bibtex, os.path.abspath(self._path(self.mybib)))
        self.assertEqual(config.filesdir, os.path.abspath(self._path(self.filesdir)))
        self.papers(f'install --local --edit --bibtex {self.mybib}XX')
        config = Config.load(self._path(".papers/config.json"))
        self.assertEqual(config.bibtex, os.path.abspath(self._path(self.mybib + "XX")))
        # The files folder from previous install is remembered
        self.assertEqual(config.filesdir, os.path.abspath(self._path(self.filesdir)))
        self.assertFalse(config.git)

    def test_install_interactive(self):
        # fully interactive install
        sp.check_call(f"""{PAPERSCMD} install --local << EOF
{self.mybib}
{self.filesdir}
n
EOF""", shell=True, cwd=self.temp_dir.name)
        self.assertTrue(self._exists(".papers/config.json"))
        self.assertTrue(self._exists(self.mybib))
        self.assertTrue(self._exists(self.filesdir))
        config = Config.load(self._path(".papers/config.json"))
        self.assertEqual(config.bibtex, os.path.abspath(self._path(self.mybib)))
        self.assertEqual(config.filesdir, os.path.abspath(self._path(self.filesdir)))
        self.assertFalse(config.git)

        # Now try simple carriage return (select default)
        sp.check_call(f"""{PAPERSCMD} install --local << EOF

e



EOF""", shell=True, cwd=self.temp_dir.name)
        self.assertTrue(self._exists(".papers/config.json"))
        self.assertTrue(self._exists(self.mybib))
        self.assertTrue(self._exists(self.filesdir))
        config = Config.load(self._path(".papers/config.json"))
        self.assertEqual(config.bibtex, os.path.abspath(self._path(self.mybib)))
        self.assertEqual(config.filesdir, os.path.abspath(self._path(self.filesdir)))

        # edit existing install (--edit)
        sp.check_call(f"""{PAPERSCMD} install --local --bibtex {self.mybib}XX << EOF
e
y
n
EOF""", shell=True, cwd=self.temp_dir.name)
        config = Config.load(self._path(".papers/config.json"))
        self.assertEqual(config.bibtex, os.path.abspath(self._path(self.mybib + "XX")))
        # The files folder from previous install is remembered
        self.assertEqual(config.filesdir, os.path.abspath(self._path(self.filesdir)))
        self.assertFalse(config.git)

        # overwrite existing install (--force)
        sp.check_call(f"""{PAPERSCMD} install --local --bibtex {self.mybib}XX << EOF
o
y
n
EOF""", shell=True, cwd=self.temp_dir.name)
        config = Config.load(self._path(".papers/config.json"))
        self.assertEqual(config.bibtex, os.path.abspath(self._path(self.mybib + "XX")))
        # The files folder from previous install was forgotten
        self.assertEqual(config.filesdir, os.path.abspath(self._path("files")))
        self.assertFalse(config.git)

        # reset default values from install
        sp.check_call(f"""{PAPERSCMD} install --local << EOF
e
reset
reset
n
EOF""", shell=True, cwd=self.temp_dir.name)
        config = Config.load(self._path(".papers/config.json"))
        self.assertEqual(config.bibtex, None)
        # The files folder from previous install was forgotten
        self.assertEqual(config.filesdir, None)
        self.assertFalse(config.git)

        # install with git tracking
        sp.check_call(f"""{PAPERSCMD} install --local << EOF
e


y
y
EOF""", shell=True, cwd=self.temp_dir.name)
        config = Config.load(self._path(".papers/config.json"))
        ## by default another bib is detected, because it starts with a (sorted)
        self.assertEqual(config.bibtex, os.path.abspath(self._path(self.anotherbib)))
        # The files folder from previous install was forgotten
        self.assertEqual(config.filesdir, os.path.abspath(self._path("files")))
        self.assertTrue(config.git)
        self.assertTrue(config.gitlfs)


class TestInstallNewBibTex(TestBaseInstall):

    # no bibtex file is present at start
    initial_content = None
    anotherbib_content = None

    def test_install(self):
        self.assertFalse(self._exists(self.mybib))
        self.assertFalse(self._exists(self.anotherbib))
        self.papers(f"""install --local --filesdir files << EOF
e
my.bib
EOF""")


class TestInstallEditor(TestBaseInstall):

    # no bibtex file is present at start
    initial_content = None
    anotherbib_content = None

    def test_install(self):
        self.papers(f'install --force --local --editor "subl -w"')
        config = Config.load(self._path(".papers/config.json"))
        self.assertEqual(config.editor, "subl -w")


class TestDefaultLocal(LocalInstallTest):
    def test_install(self):
        self.assertTrue(self._exists(".papers/config.json"))
        self.assertTrue(self.config.local)
        self.papers(f'install --edit')
        self.assertTrue(self._exists(".papers/config.json"))
        config = Config.load(self._path(".papers/config.json"))
        self.assertTrue(config.local)

class TestDefaultLocal2(GlobalInstallTest):
    def test_install(self):
        self.assertTrue(self._exists(CONFIG_FILE))
        self.assertFalse(self.config.local)
        self.papers(f'install --edit')
        self.assertTrue(self._exists(CONFIG_FILE))
        config = Config.load(CONFIG_FILE)
        self.assertFalse(config.local)


class TestGlobalInstall(TestBaseInstall):

    def test_install(self):
        self.assertFalse(self._exists(self.mybib))
        self.assertFalse(self._exists(self.filesdir))
        self.assertFalse(os.path.exists(CONFIG_FILE))
        self.papers(f'install --no-prompt --bibtex {self.mybib} --files {self.filesdir}')
        self.assertTrue(self._exists(self.mybib))
        self.assertTrue(self._exists(self.filesdir))
        self.assertTrue(os.path.exists(CONFIG_FILE))
        config = Config.load(self._path(CONFIG_FILE))
        self.assertEqual(config.bibtex, os.path.abspath(self._path(self.mybib)))
        self.assertEqual(config.filesdir, os.path.abspath(self._path(self.filesdir)))


class TestGitInstall(TestBaseInstall):

    def test_install_gitlfs(self):
        self.papers(f'install --local --no-prompt --git-lfs')
        config = Config.load(self._path(".papers/config.json"))
        self.assertTrue(config.git)
        # self.assertTrue(self._exists(".git"))

    def test_install(self):
        self.papers(f'install --local --no-prompt --bibtex {self.mybib} --files {self.filesdir} --git')
        self.assertTrue(self._exists(self.mybib))
        # self.assertTrue(self._exists(".git"))
        # count = sp.check_output(f'cd {self.temp_dir.name} && git rev-list --all --count', shell=True).strip().decode()
        # self.assertEqual(count, '0')
        count = self.papers('git rev-list --all --count', sp_cmd='check_output')
        count_ = sp.check_output("git rev-list --all --count", shell=True, cwd=self._path('.papers')).decode().strip()
        self.assertEqual(count, count_)
        count2 = self.papers('git rev-list --all --count', sp_cmd='check_output')
        count2_ = sp.check_output("git rev-list --all --count", shell=True, cwd=self._path('.papers')).decode().strip()
        self.assertEqual(count2, count2_)
        self.papers(f'add {self.anotherbib}')
        # self.papers(f'add --doi 10.5194/bg-8-515-2011')
        count2 = self.papers('git rev-list --all --count', sp_cmd='check_output')

        print(count, count2)
        self.assertEqual(int(count2), int(count)+1)

    def test_install_interactive(self):
        self.papers(f"""install --local --filesdir files --bibtex bibbib.bib << EOF
y
y
EOF""")
        config = Config.load(self._path(".papers/config.json"))
        self.assertTrue(config.git)
        self.assertTrue(config.gitlfs)

    def test_install_interactive2(self):
        self.papers(f"""install --local --filesdir files --bibtex bibbib.bib << EOF
y
n
EOF""")
        config = Config.load(self._path(".papers/config.json"))
        self.assertTrue(config.git)
        self.assertFalse(config.gitlfs)

    def test_install_interactive3(self):
        self.papers(f"""install --local --filesdir files --bibtex bibbib.bib << EOF
n
EOF""")
        config = Config.load(self._path(".papers/config.json"))
        self.assertFalse(config.git)
        self.assertFalse(config.gitlfs)

    def test_install_interactive4(self):
        self.papers(f"""install --local --filesdir files --bibtex bibbib.bib << EOF

EOF""")
        config = Config.load(self._path(".papers/config.json"))
        self.assertFalse(config.git)
        self.assertFalse(config.gitlfs)

    def test_install_interactive5(self):
        self.papers(f"""install --local --filesdir files --bibtex bibbib.bib << EOF
y

EOF""")
        config = Config.load(self._path(".papers/config.json"))
        self.assertTrue(config.git)
        self.assertFalse(config.gitlfs)


class TestUndoGitLocal(TestBaseInstall):

    def _install(self):
        self.papers(f'install --local --no-prompt --bibtex {self.mybib} --files {self.filesdir} --git --git-lfs')


    def test_undo(self):
        self._install()

        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 0)
        self.papers(f'add {self.anotherbib}')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 1)

        open(self._path('yetanother'), 'w').write(bibtex2)
        self.papers(f'add yetanother')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 2)

        self.papers(f'undo')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 1)

        self.papers(f'undo')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 0)

        self.papers(f'redo')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 1)

        self.papers(f'redo')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 2)

        self.papers(f'redo')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 2)


class TestUndoGitOnlyLocal(TestUndoGitLocal):
    def _install(self):
        self.papers(f'install --local --no-prompt --bibtex {self.mybib} --files {self.filesdir} --git')


class TestUndoGitGlobal(TestUndoGitLocal):

    def _install(self):
        self.papers(f'install --no-prompt --bibtex {self.mybib} --files {self.filesdir} --git --git-lfs')


class TestUndoNoInstall(TestBaseInstall):

    def test_undo(self):

        open(self._path(self.mybib), 'w').write('')

        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 0)
        self.papers(f'add {self.anotherbib}  --bibtex {self.mybib} --files {self.filesdir}')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 1)

        open(self._path('yetanother'), 'w').write(bibtex2)
        self.papers(f'add yetanother --bibtex {self.mybib} --files {self.filesdir}')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 2)

        self.papers(f'undo --bibtex {self.mybib} --files {self.filesdir}')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 1)

        self.papers(f'undo --bibtex {self.mybib} --files {self.filesdir}')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 2)

        self.papers(f'redo --bibtex {self.mybib} --files {self.filesdir}')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 1)

        self.papers(f'redo --bibtex {self.mybib} --files {self.filesdir}')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 2)

        self.papers(f'redo --bibtex {self.mybib} --files {self.filesdir}')
        biblio = Biblio.load(self._path(self.mybib), '')
        self.assertEqual(len(biblio.entries), 1)



class TestUninstall(LocalInstallTest):
    def test_uninstall(self):
        self.assertTrue(self._exists(".papers/config.json"))
        self.papers(f'uninstall')
        self.assertFalse(self._exists(".papers/config.json"))


class TestUninstall2(GlobalInstallTest):
    def test_uninstall(self):
        self.assertTrue(self._exists(CONFIG_FILE))
        self.papers(f'install --force --local')
        self.assertTrue(self._exists(".papers/config.json"))
        self.assertTrue(self._exists(CONFIG_FILE))
        self.papers(f'uninstall')
        self.assertFalse(self._exists(".papers/config.json"))
        self.assertTrue(self._exists(CONFIG_FILE))

    def test_uninstall(self):
        self.papers(f'install --force --local')
        self.assertTrue(self._exists(".papers/config.json"))
        self.assertTrue(self._exists(CONFIG_FILE))
        self.papers(f'uninstall --recursive')
        self.assertFalse(self._exists(".papers/config.json"))
        self.assertFalse(self._exists(CONFIG_FILE))