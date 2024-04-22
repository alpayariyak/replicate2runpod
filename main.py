from replicate import get_docker_commands
from runpod_utils import create_pod
from utils import load_tokens
import runpod
import requests
import os
import json
os.environ['WDM_LOG'] = '0'

def main():
    runpod_token, hf_token = load_tokens()
    runpod.api_key = runpod_token
    url = input("\n\nEnter the Replicate URL: ")
    docker_commands = get_docker_commands(url)
    if not docker_commands:
        print("\n\nDocker page not found for this Replicate space.")
        exit()
    image_name = docker_commands['docker_run_command'].split(' ')[-1]
    
    pod = create_pod(
        name=url.split('/')[-1],
        image_name=image_name,
        gpu_type_id="NVIDIA A100 80GB PCIe",
        cloud_type='SECURE',
        volume_in_gb=0,
        gpu_count=1,
        container_disk_in_gb=200,
        env={
            'HF_TOKEN': hf_token
        }
    )
    print(f"\n\nPod created with ID: {pod['id']}")
    URL = f"https://{pod['id']}-5000.proxy.runpod.net"
    
    # Wait until url is ready
    print("\n\nWaiting for the API to be ready...")
    while True:
        try:
            response = requests.get(URL + '/predictions')
            if response.status_code == 405:
                break
        except:
            pass

    json_data_str = docker_commands['example_command'].split('-d ')[1]
    json_data_str = json_data_str[json_data_str.index('{') : json_data_str.rindex('}')+1].replace('\n', '')
    input_dict = json.loads(json_data_str)  

    while True:
        print("\n\n### OPTIONS:")
        print("1. Send a request")
        print("2. Show usage example")
        print("3. Exit")
        choice = input("Select an option (1, 2, or 3): ")

        if choice == '1':
            # Ask user to input each value
            print("\n\n### SENDING REQUEST:")
            for key in input_dict['input']:
                val = input(f"\n{key} (Leave empty for default: {input_dict['input'][key]}): ")
                if len(val) > 0:
                    input_dict['input'][key] = val
            # Send request
            response = requests.post(URL + '/predictions', json=input_dict)
            print("\n\n### RESPONSE:")
            # Print the json in a pretty format
            print(json.dumps(response.json(), indent=4))
        elif choice == '2':
            # Show usage example
            print("\n\n### USAGE EXAMPLE:")
            print(f"curl -s -X POST \\\n  -H \"Content-Type: application/json\" \\\n  -d $'{json.dumps(input_dict, indent=2)}' \\\n  {URL}/predictions")
        elif choice == '3':
            print("\n\nExiting...")
            break
        else:
            print("\n\nInvalid option, please try again.")


if __name__ == '__main__':
    main()
    

