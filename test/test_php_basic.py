from unit.control import TestControl


class TestPHPBasic(TestControl):
    prerequisites = {'modules': {'php': 'any'}}

    conf_app = {
        "app": {
            "type": "php",
            "processes": {"spare": 0},
            "root": "/app",
            "index": "index.php",
        }
    }

    conf_basic = {
        "listeners": {"*:7080": {"pass": "applications/app"}},
        "applications": conf_app,
    }

    def test_php_get_applications(self):
        self.conf(self.conf_app, 'applications')

        conf = self.conf_get()

        self.assertEqual(conf['listeners'], {}, 'listeners')
        self.assertEqual(
            conf['applications'],
            {
                "app": {
                    "type": "php",
                    "processes": {"spare": 0},
                    "root": "/app",
                    "index": "index.php",
                }
            },
            'applications',
        )

        self.assertEqual(
            self.conf_get('applications'),
            {
                "app": {
                    "type": "php",
                    "processes": {"spare": 0},
                    "root": "/app",
                    "index": "index.php",
                }
            },
            'applications prefix',
        )

        self.assertEqual(
            self.conf_get('applications/app'),
            {
                "type": "php",
                "processes": {"spare": 0},
                "root": "/app",
                "index": "index.php",
            },
            'applications prefix 2',
        )

        self.assertEqual(self.conf_get('applications/app/type'), 'php', 'type')
        self.assertEqual(
            self.conf_get('applications/app/processes/spare'),
            0,
            'spare processes',
        )

    def test_php_get_listeners(self):
        self.conf(self.conf_basic)

        self.assertEqual(
            self.conf_get()['listeners'],
            {"*:7080": {"pass": "applications/app"}},
            'listeners',
        )

        self.assertEqual(
            self.conf_get('listeners'),
            {"*:7080": {"pass": "applications/app"}},
            'listeners prefix',
        )

        self.assertEqual(
            self.conf_get('listeners/*:7080'),
            {"pass": "applications/app"},
            'listeners prefix 2',
        )

    def test_php_change_listener(self):
        self.conf(self.conf_basic)
        self.conf({"*:7081": {"pass": "applications/app"}}, 'listeners')

        self.assertEqual(
            self.conf_get('listeners'),
            {"*:7081": {"pass": "applications/app"}},
            'change listener',
        )

    def test_php_add_listener(self):
        self.conf(self.conf_basic)
        self.conf({"pass": "applications/app"}, 'listeners/*:7082')

        self.assertEqual(
            self.conf_get('listeners'),
            {
                "*:7080": {"pass": "applications/app"},
                "*:7082": {"pass": "applications/app"},
            },
            'add listener',
        )

    def test_php_change_application(self):
        self.conf(self.conf_basic)

        self.conf('30', 'applications/app/processes/max')
        self.assertEqual(
            self.conf_get('applications/app/processes/max'),
            30,
            'change application max',
        )

        self.conf('"/www"', 'applications/app/root')
        self.assertEqual(
            self.conf_get('applications/app/root'),
            '/www',
            'change application root',
        )

    def test_php_delete(self):
        self.conf(self.conf_basic)

        self.assertIn('error', self.conf_delete('applications/app'))
        self.assertIn('success', self.conf_delete('listeners/*:7080'))
        self.assertIn('success', self.conf_delete('applications/app'))
        self.assertIn('error', self.conf_delete('applications/app'))

    def test_php_delete_blocks(self):
        self.conf(self.conf_basic)

        self.assertIn('success', self.conf_delete('listeners'))
        self.assertIn('success', self.conf_delete('applications'))

        self.assertIn('success', self.conf(self.conf_app, 'applications'))
        self.assertIn(
            'success',
            self.conf({"*:7081": {"pass": "applications/app"}}, 'listeners'),
            'applications restore',
        )


if __name__ == '__main__':
    TestPHPBasic.main()
