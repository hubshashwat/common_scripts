import hvac

MOUNT_POINT = ''  # mount point - can be fleet/stack level or a single level

client = hvac.Client(
    url='https://vault.enterprise.company.co/',
    token=''  # token you copy from UI
)
client.secrets.kv.v2.configure(
    mount_point=MOUNT_POINT
)

# Check if the client is authenticated
if not client.is_authenticated():
    raise Exception("Vault authentication failed")

clients = ['test1', 'test2']

for _client in clients:
    # Define the path to the secret
    secret_path = f'se/services/{_client}/sftp/'
    try:
        # Read the username from the specified path
        response = client.secrets.kv.v2.list_secrets(path=secret_path, mount_point=MOUNT_POINT)
        username = response['data']['keys']
        for each_username in username:
            # retrieve from vault
            response = client.secrets.kv.v2.read_secret_version(
                path=secret_path + each_username, mount_point=MOUNT_POINT)['data']['data']
            print(response)
            # update from vault
            response['host'] = "new-host"
            response['port'] = "22"
            client.secrets.kv.v2.create_or_update_secret(path=secret_path + each_username, secret=response,
                                                         mount_point=MOUNT_POINT)
            print(f'update successful for: {each_username}')
    except Exception as exc:
        print(exc)
