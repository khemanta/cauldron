import os
import json
from unittest.mock import patch

import cauldron as cd
from cauldron.test import support
from cauldron.test.support import scaffolds
from cauldron import environ


class TestCreate(scaffolds.ResultsTest):
    """

    """

    def test_create_no_args(self):
        """
        """

        r = support.create_project(self, '', '')
        self.assertTrue(r.failed, 'should have failed')

    def test_create_no_path(self):
        """
        """

        r = support.create_project(self, 'test_create', '')
        self.assertTrue(r.failed, 'should have failed')

    def test_create_simple_success(self):
        """
        """

        r = support.create_project(self, 'test_create')

        self.assertFalse(
            r.failed,
            support.Message(
                'Failed to create project',
                response=r
            )
        )

        path = os.path.join(r.data['source_directory'], 'cauldron.json')
        self.assertTrue(
            os.path.exists(path),
            support.Message(
                'No project found',
                'Missing cauldron.json file that should exist when a new',
                'project is created',
                response=r,
                path=path
            )
        )

    def test_create_twice(self):
        """
        """

        r1 = support.create_project(self, 'test_create')
        r1.identifier = 'First {}'.format(r1.identifier)

        r2 = support.create_project(self, 'test_create')
        r2.identifier = 'Second {}'.format(r2.identifier)

        self.assertTrue(
            r2.failed,
            support.Message(
                'No second project',
                'It should not be possible to create a second project in the',
                'same location',
                response=[r1, r2]
            )
        )

    def test_create_full_success(self):
        """
        """

        r = support.create_project(
            self,
            'test_create',
            title='This is a test',
            summary='More important information goes in this spot',
            author='Kermit the Frog'
        )

        self.assertFalse(
            r.failed,
            'Failed to create project\n:{}'.format(r.echo())
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(r.data['source_directory'], 'cauldron.json')
            ),
            'Missing cauldron.json in new project folder\n:{}'.format(r.echo())
        )

    def test_autocomplete(self):
        """

        :return:
        """

        alias = 'ex'
        path = environ.paths.resources('examples')
        support.run_command(
            'alias add "{}" "{}" --temporary'.format(alias, path)
        )

        result = support.autocomplete('create my_project @home:')
        self.assertIsNotNone(
            result,
            support.Message(
                'autocomplete result should not be None',
                result=result
            )
        )

        # Get all directories in the examples folder
        items = [(e, os.path.join(path, e)) for e in os.listdir(path)]
        items = [e for e in items if os.path.isdir(e[1])]

        result = support.autocomplete('create my_project @ex:')
        self.assertEqual(
            len(result), len(items),
            support.Message(
                'should autocomplete from the examples folder',
                result=result,
                items=items
            )
        )

        hellos = [e for e in items if e[0].startswith('hell')]
        result = support.autocomplete('create my_project @ex:hell')
        self.assertEqual(
            len(result), len(hellos),
            support.Message(
                'should autocomplete examples that start with "hell"',
                result=result,
                items=items
            )
        )

    def test_folders(self):
        """ should create libs and assets folders in project """

        libs_folder = 'libs_folder'
        assets_folder = 'assets_folder'

        result = support.create_project(
            self,
            'marcus',
            libs=libs_folder,
            assets=assets_folder
        )
        self.assertFalse(result.failed)

        project = cd.project.internal_project

        items = os.listdir(project.source_directory)

        self.assertIn(libs_folder, items)
        self.assertIn(assets_folder, items)

        self.assertIn(libs_folder, project.settings.fetch('library_folders'))
        self.assertIn(assets_folder, project.settings.fetch('asset_folders'))

        with open(project.source_path, 'r+') as f:
            data = json.load(f)

        self.assertEqual(libs_folder, data['library_folders'][0])
        self.assertEqual(assets_folder, data['asset_folders'][0])

        support.run_command('close')

    def test_write_fail(self):
        """ should fail if directory cannot be written """

        target = 'cauldron.cli.commands.create.write_project_data'
        with patch(target) as func:
            func.return_value = False
            result = support.create_project(self, 'aurelius')

        self.assertTrue(result.failed)

        support.run_command('close')

    def test_create_fail(self):
        """ should fail if directory cannot be created """

        target = 'cauldron.cli.commands.create.create_project_directory'
        with patch(target) as func:
            func.return_value = False
            result = support.create_project(self, 'augustus')

        self.assertTrue(result.failed)

        support.run_command('close')
