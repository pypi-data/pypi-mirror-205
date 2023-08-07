import json
import argparse


def parse(pylama_json_output: str):
    # Load json from string
    pylama_json = json.loads(pylama_json_output)
    
    # Create a list comprehension to construct a list of result dictionaries
    results = [{
        'type': 'issue',
        'check_name': line['number'],
        'description': line['message'],
        'categories': [line['source']],
        'location': {
            'path': line['filename'],
            'lines': {
                'begin': line['lnum'],
                'end': line['lnum']
            }
        },
        'severity': {'E': 'major', 'W': 'minor'}.get(line['etype'], 'E'),
        'engine_name': line['source']
    } for line in pylama_json]
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Convert pylama output to codeclimate format')
    parser.add_argument('-o', default='-', type=str, help='output filename')
    parser.add_argument('-i', default='-', type=str, help='input filename')
    args = parser.parse_args()
    in_file = args.i
    out_file = args.o

    # read input file
    with open(in_file) as f:
        pylama_json_output = f.read()
        
    results = parse(pylama_json_output)
    raw_results = json.dumps(results, indent=2)

    if out_file == '-':
        print(raw_results)
    else:
        with open(out_file, 'w') as f:
            f.write(raw_results)


if __name__ == '__main__':
    main()
