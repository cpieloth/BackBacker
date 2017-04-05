"""Custom commands for setup.py"""

import abc
import distutils.cmd
import os
import re

__author__ = 'Christof Pieloth'

working_dir = os.path.abspath(os.path.dirname(__file__))
build_dir = os.path.join(working_dir, 'build')

api_name = 'backbacker'
project_name = re.search('^__project_name__\s*=\s*\'(.*)\'',
                         open(os.path.join(working_dir, api_name, '__init__.py')).read(), re.M).group(1)
version = re.search('^__version__\s*=\s*\'(.*)\'',
                    open(os.path.join(working_dir, api_name, '__init__.py')).read(), re.M).group(1)


class CustomCommand(distutils.cmd.Command, metaclass=abc.ABCMeta):
    """Base class for all custom commands."""

    @staticmethod
    def description(desc):
        """
        Generate description text.

        :param desc: Description.
        :return: Text for description.
        :rtype: str
        """
        return '{}: {}'.format(api_name.upper(), desc)

    @classmethod
    @abc.abstractmethod
    def name(cls):
        """
        Return name of the command.

        :return: Name of the command.
        :rtype: str
        """
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def clean_folders(cls):
        """
        Return list of folders to clean-up.

        :return: List of folders.
        :rtype: list
        """
        raise NotImplementedError()


class PackageCustomCmd(CustomCommand):
    """Create a Python Built Distribution package."""

    description = CustomCommand.description(__doc__)
    user_options = []

    @classmethod
    def clean_folders(cls):
        return [os.path.join(working_dir, 'dist'),
                os.path.join(working_dir, 'temp'),
                os.path.join(working_dir, '{}.egg-info'.format(project_name)),
                os.path.join(working_dir, 'build', 'lib'),  # do not use variable build_dir
                os.path.join(working_dir, 'build', 'bdist*')  # do not use variable build_dir
                ]

    @classmethod
    def name(cls):
        return 'package'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from setuptools import sandbox
        sandbox.run_setup('setup.py', ['bdist_wheel', '--python-tag', 'py3'])


class DocApiCustomCmd(CustomCommand):
    """Create API documentation with Sphinx."""

    description = CustomCommand.description(__doc__)
    user_options = []

    sphinx_build_dir = os.path.join(build_dir, 'sphinx')
    doc_build_dir = os.path.join(build_dir, 'doc', 'api')

    @classmethod
    def clean_folders(cls):
        return [cls.doc_build_dir, cls.sphinx_build_dir]

    @classmethod
    def name(cls):
        return 'doc_api'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sphinx.apidoc
        import sphinx.cmdline

        # generate source files for Sphinx from python code
        argv = ['sphinx-apidoc', '-f', '-o', self.sphinx_build_dir, os.path.join(working_dir, api_name)]
        sphinx.apidoc.main(argv)

        # copy configuration and source files to build folder, to keep doc/sphinx clean
        self.copy_tree(os.path.join(working_dir, 'doc', 'sphinx'), self.sphinx_build_dir)

        # generate HTML
        argv = ['sphinx-build', '-b', 'html', '-a', self.sphinx_build_dir, self.doc_build_dir]
        return sphinx.cmdline.main(argv)


class DocManualCustomCmd(CustomCommand):
    """Create HTML manual/user documentation from Markdown."""

    description = CustomCommand.description(__doc__)
    user_options = []

    dst_dir = os.path.join(build_dir, 'doc', 'manual')
    resource_dst_dir = os.path.join(dst_dir, 'resources')

    @classmethod
    def name(cls):
        return 'doc_manual'

    @classmethod
    def clean_folders(cls):
        return [cls.dst_dir, cls.resource_dst_dir]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import markdown
        import string

        template_fname = os.path.join(working_dir, 'doc', 'html', 'template_manual.html')
        src_dir = os.path.join(working_dir, 'doc', 'manual')
        src_parts = src_dir.split(os.path.sep)
        resource_src_dir = os.path.join(src_dir, 'resources')

        # copy resource folder to destination
        if os.path.exists(resource_src_dir):
            self.copytree(resource_src_dir, self.resource_dst_dir)

        # load HTML template
        with open(template_fname, 'r') as fd:
            template = string.Template(fd.read())

        # generate HTML for *.md and write it to dst_dir
        md = markdown.Markdown(output_format='html')
        for root, _, files in os.walk(src_dir):
            # get sub folder to create
            root_parts = root.split(os.path.sep)
            sub_folders = []
            if len(root_parts) > len(src_parts):
                sub_folders.extend(root_parts[len(src_parts):])

            for fname in files:
                if not fname.endswith('.md'):
                    continue

                with open(os.path.join(root, fname)) as fd:
                    html = md.convert(fd.read())

                # create destination path/sub folder
                html_path = os.path.join(self.dst_dir, *sub_folders)
                os.makedirs(html_path, exist_ok=True)

                html_fname = fname.replace(' ', '')[:-3]  # remove .md
                with open('{}.html'.format(os.path.join(html_path, html_fname)), 'w') as fd:
                    fd.write(template.substitute(content=html))


class DocumentationCustomCmd(CustomCommand):
    """Create API and manual documentation."""

    description = CustomCommand.description(__doc__)
    user_options = []

    @classmethod
    def name(cls):
        return 'documentation'

    @classmethod
    def clean_folders(cls):
        return [os.path.join(build_dir, 'doc')]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command('doc_api')
        self.run_command('doc_manual')


class CheckCodeCustomCmd(CustomCommand):
    """Run code analysis with pylint."""

    description = CustomCommand.description(__doc__)
    user_options = []

    @classmethod
    def name(cls):
        return 'check_code'

    @classmethod
    def clean_folders(cls):
        return []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from pylint.lint import Run
        args = ['--rcfile', os.path.join(working_dir, 'tools', 'pylintrc'), os.path.join(working_dir, api_name)]
        return Run(args, exit=False).linter.msg_status


class CheckStyleCodeCustomCmd(CustomCommand):
    """Run style checker for code with pep8."""

    description = CustomCommand.description(__doc__)
    user_options = []

    @classmethod
    def name(cls):
        return 'check_style_code'

    @classmethod
    def clean_folders(cls):
        return []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import pep8

        ignores = list()
        ignores.append('E501')  # E501: line too long

        style_guide = pep8.StyleGuide(ignore=ignores)
        report = style_guide.check_files([os.path.join(working_dir, api_name), os.path.join(working_dir, 'tests')])
        return report.total_errors


class CheckStyleDocCustomCmd(CustomCommand):
    """Run style checker for docstrings with pep257."""

    description = CustomCommand.description(__doc__)
    user_options = []

    @classmethod
    def name(cls):
        return 'check_style_doc'

    @classmethod
    def clean_folders(cls):
        return []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import pep257
        import sys

        ignores = list()
        ignores.append('D105')  # Missing docstring in magic method
        ignores.append('D203')  # 1 blank line required before class docstring

        sys.argv = ['pep257', '--ignore={}'.format(','.join(ignores)), os.path.join(working_dir, api_name)]
        return pep257.run_pep257()


class CheckStyleCustomCmd(CustomCommand):
    """Run style checkers."""

    description = CustomCommand.description(__doc__)
    user_options = []

    @classmethod
    def name(cls):
        return 'check_style'

    @classmethod
    def clean_folders(cls):
        return []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command('check_style_code')
        self.run_command('check_style_doc')


class TestCustomCmd(CustomCommand):
    """Run unit tests."""

    description = CustomCommand.description(__doc__)
    user_options = []

    @classmethod
    def name(cls):
        return 'test'

    @classmethod
    def clean_folders(cls):
        return []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import unittest
        argv = ['unittest', 'discover', os.path.join(working_dir, 'tests', api_name)]
        return unittest.main(argv=argv, module=None, exit=False).result


class CoverageCustomCmd(CustomCommand):
    """Generate unit test coverage report."""

    description = CustomCommand.description(__doc__)
    user_options = []

    dst_dir = os.path.join(build_dir, 'coverage_html')

    @classmethod
    def name(cls):
        return 'coverage'

    @classmethod
    def clean_folders(cls):
        return [cls.dst_dir, os.path.join(working_dir, '.coverage')]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from coverage.cmdline import main

        tests_dir = os.path.join(working_dir, 'tests', api_name)
        argv = ['run', '--source', 'example/', '-m', 'unittest', 'discover', tests_dir]
        rc = main(argv)
        if rc != 0:
            return rc

        argv = ['html', '-d', self.dst_dir]
        return main(argv)


class CleanCustomCmd(CustomCommand):
    """Extends standard clean command to clean-up fiels and folders of custom commands."""
    user_options = []

    @classmethod
    def name(cls):
        return 'clean'

    @classmethod
    def clean_folders(cls):
        return []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # invoke the default clean()
        import shutil
        from distutils.command.clean import clean
        c = clean(self.distribution)
        c.all = True
        c.finalize_options()
        c.run()

        pycache_folders = [root for root, _, _ in os.walk(working_dir) if root.endswith('__pycache__')]
        custom_folders = [folder for cmd in custom_commands.values() for folder in cmd.clean_folders()]

        # additional cleanup
        for folder in pycache_folders + custom_folders:
            try:
                if os.path.isfile(folder):
                    os.remove(folder)
                else:
                    shutil.rmtree(folder)
            except:
                pass


custom_commands = {
    PackageCustomCmd.name(): PackageCustomCmd,
    DocApiCustomCmd.name(): DocApiCustomCmd,
    DocManualCustomCmd.name(): DocManualCustomCmd,
    DocumentationCustomCmd.name(): DocumentationCustomCmd,
    CheckCodeCustomCmd.name(): CheckCodeCustomCmd,
    CheckStyleCodeCustomCmd.name(): CheckStyleCodeCustomCmd,
    CheckStyleDocCustomCmd.name(): CheckStyleDocCustomCmd,
    CheckStyleCustomCmd.name(): CheckStyleCustomCmd,
    TestCustomCmd.name(): TestCustomCmd,
    CoverageCustomCmd.name(): CoverageCustomCmd,
    CleanCustomCmd.name(): CleanCustomCmd,
}
