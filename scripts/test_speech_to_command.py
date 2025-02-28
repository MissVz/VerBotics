import unittest
import json
from speech_to_command import validate_command, process_command

class TestSpeechToCommand(unittest.TestCase):

    def test_validate_command_speed(self):
        """Test speed validation within -150 to 150 range"""
        command = {"parameters": {"angle": 0, "speed": 200, "duration": 2}}
        validated = validate_command(command)
        self.assertEqual(validated["parameters"]["speed"], 150)

        command["parameters"]["speed"] = -200
        validated = validate_command(command)
        self.assertEqual(validated["parameters"]["speed"], -150)

    def test_validate_command_angle(self):
        """Test angle validation between 0 and 360"""
        command = {"parameters": {"angle": 400, "speed": 100, "duration": 2}}
        validated = validate_command(command)
        self.assertEqual(validated["parameters"]["angle"], 0)

        command["parameters"]["angle"] = -10
        validated = validate_command(command)
        self.assertEqual(validated["parameters"]["angle"], 0)

    def test_validate_command_duration(self):
        """Test duration validation between 1 and 10 seconds"""
        command = {"parameters": {"angle": 0, "speed": 100, "duration": 0.1}}
        validated = validate_command(command)
        self.assertEqual(validated["parameters"]["duration"], 1)

        command["parameters"]["duration"] = 15
        validated = validate_command(command)
        self.assertEqual(validated["parameters"]["duration"], 10)

    def test_process_command_json_format(self):
        """Ensure process_command returns valid JSON format"""
        spoken_text = "Move forward quickly"
        response = process_command(spoken_text)
        
        try:
            parsed_json = json.loads(response)
            self.assertIn("command", parsed_json)
            self.assertIn("parameters", parsed_json)
            self.assertIn("angle", parsed_json["parameters"])
            self.assertIn("speed", parsed_json["parameters"])
            self.assertIn("duration", parsed_json["parameters"])
        except json.JSONDecodeError:
            self.fail("process_command() did not return valid JSON.")

if __name__ == "__main__":
    unittest.main()