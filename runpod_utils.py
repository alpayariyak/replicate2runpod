
import runpod
def create_template(name, image_name, env,container_disk_in_gb, is_serverless=False):
    return runpod.create_template(
        name=name,
        image_name=image_name,
        container_disk_in_gb=container_disk_in_gb,
        env=env,
        is_serverless=is_serverless
    )

def create_pod(name, image_name, gpu_type_id, cloud_type, gpu_count, volume_in_gb, container_disk_in_gb, env, allowed_cuda_versions=None):
    return runpod.create_pod(
        name=name,
        image_name=image_name,
        gpu_type_id=gpu_type_id,
        cloud_type=cloud_type,
        gpu_count=gpu_count,
        volume_in_gb=volume_in_gb,
        container_disk_in_gb=container_disk_in_gb,
        ports="5000/http,22/tcp",
        env=env
        )

def get_gpu_types():
    return runpod.get_gpus()

