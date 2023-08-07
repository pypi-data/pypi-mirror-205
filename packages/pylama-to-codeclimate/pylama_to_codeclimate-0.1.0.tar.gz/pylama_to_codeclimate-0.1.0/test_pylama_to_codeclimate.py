from pylama_to_codeclimate import parse


def test_parse():
    pylama_json_output = """
    [
        {
            "filename": "file1.py",
            "lnum": 1,
            "etype": "E",
            "number": "E123",
            "message": "Error message",
            "source": "pylama"
        },
        {
            "filename": "file2.py",
            "lnum": 5,
            "etype": "W",
            "number": "W456",
            "message": "Warning message",
            "source": "pylama"
        }
    ]
    """
    expected_results = [
        {
            'type': 'issue',
            'check_name': 'E123',
            'description': 'Error message',
            'categories': ['pylama'],
            'location': {
                'path': 'file1.py',
                'lines': {
                    'begin': 1,
                    'end': 1
                }
            },
            'severity': 'major',
            'engine_name': 'pylama'
        },
        {
            'type': 'issue',
            'check_name': 'W456',
            'description': 'Warning message',
            'categories': ['pylama'],
            'location': {
                'path': 'file2.py',
                'lines': {
                    'begin': 5,
                    'end': 5
                }
            },
            'severity': 'minor',
            'engine_name': 'pylama'
        }
    ]
    results = parse(pylama_json_output)
    assert results == expected_results
