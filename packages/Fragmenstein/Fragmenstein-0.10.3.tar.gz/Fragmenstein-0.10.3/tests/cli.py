import unittest
import subprocess

class CliTests(unittest.TestCase):

    def command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return out, err, process.returncode


