import os
import unittest
import utils

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.environ.get("IMAGE_DIR") or os.path.join(CURRENT_DIR, "..")


def get_dockerfile_path(image_dir):
    return os.path.join(IMAGE_DIR, image_dir)


class BaseImageTest(unittest.TestCase):

    def setUp(self):
        self.image = "confluentinc/cp-base"
        utils.build_image(self.image, get_dockerfile_path("debian/base"))

    def test_image_build(self):
        self.assertTrue(utils.image_exists(self.image))

    def test_java_install(self):
        cmd = "java -version"
        expected = 'OpenJDK Runtime Environment (Zulu 8.15.0.1-linux64) (build 1.8.0_92-b15)'
        output = utils.run_docker_command(image=self.image, command=cmd)
        self.assertTrue(expected in output)

    def test_dub_exists(self):
        self.assertTrue(utils.path_exists_in_image(self.image, "/usr/local/bin/dub"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/usr/local/bin/cub"))


class ZookeeperImageTest(unittest.TestCase):

    def setUp(self):
        self.image = "confluentinc/cp-zookeeper"
        utils.build_image(self.image, get_dockerfile_path("debian/base"))
        utils.build_image(self.image, get_dockerfile_path("debian/zookeeper"))

    def test_image_build(self):
        self.assertTrue(utils.image_exists(self.image))

    def test_zk_install(self):
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/kafka"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent"))

    def test_boot_scripts_present(self):
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent/docker/configure"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent/docker/ensure"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent/docker/launch"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent/docker/run"))
        self.assertTrue(utils.executable_exists_in_image(self.image, "/etc/confluent/docker/configure"))
        self.assertTrue(utils.executable_exists_in_image(self.image, "/etc/confluent/docker/ensure"))
        self.assertTrue(utils.executable_exists_in_image(self.image, "/etc/confluent/docker/launch"))
        self.assertTrue(utils.executable_exists_in_image(self.image, "/etc/confluent/docker/run"))

    def test_zk_commands(self):
        expected = "USAGE: /usr/bin/zookeeper-server-start [-daemon] zookeeper.properties"
        self.assertTrue(expected in utils.run_docker_command(image=self.image, command="zookeeper-server-start"))


class KafkaImageTest(unittest.TestCase):

    def setUp(self):
        self.image = "confluentinc/cp-kafka"
        utils.build_image(self.image, get_dockerfile_path("debian/base"))
        utils.build_image(self.image, get_dockerfile_path("debian/kafka"))

    def test_image_build(self):
        self.assertTrue(utils.image_exists(self.image))

    def test_zk_install(self):
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/kafka"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent"))

    def test_boot_scripts_present(self):
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent/docker/configure"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent/docker/ensure"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent/docker/launch"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent/docker/run"))
        self.assertTrue(utils.executable_exists_in_image(self.image, "/etc/confluent/docker/configure"))
        self.assertTrue(utils.executable_exists_in_image(self.image, "/etc/confluent/docker/ensure"))
        self.assertTrue(utils.executable_exists_in_image(self.image, "/etc/confluent/docker/launch"))
        self.assertTrue(utils.executable_exists_in_image(self.image, "/etc/confluent/docker/run"))

    def test_kafka_commands(self):
        expected = "USAGE: /usr/bin/kafka-server-start [-daemon] server.properties [--override property=value]*"
        self.assertTrue(expected in utils.run_docker_command(image=self.image, command="kafka-server-start"))


class ConnectImageTest(unittest.TestCase):

    def setUp(self):
        self.image = "confluentinc/cp-kafka-connect"
        utils.build_image(self.image, get_dockerfile_path("debian/base"))
        utils.build_image(self.image, get_dockerfile_path("debian/kafka"))
        utils.build_image(self.image, get_dockerfile_path("debian/kafka-connect"))

    def test_image_build(self):
        self.assertTrue(utils.image_exists(self.image))

    def test_zk_install(self):
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/kafka"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/kafka-connect"))

    def test_boot_scripts_present(self):
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent/docker/configure"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent/docker/ensure"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent/docker/launch"))
        self.assertTrue(utils.path_exists_in_image(self.image, "/etc/confluent/docker/run"))
        self.assertTrue(utils.executable_exists_in_image(self.image, "/etc/confluent/docker/configure"))
        self.assertTrue(utils.executable_exists_in_image(self.image, "/etc/confluent/docker/ensure"))
        self.assertTrue(utils.executable_exists_in_image(self.image, "/etc/confluent/docker/launch"))
        self.assertTrue(utils.executable_exists_in_image(self.image, "/etc/confluent/docker/run"))
