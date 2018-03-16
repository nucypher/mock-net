# NuCypher KMS MockNet

### Usage Instructions:
1. Install pyUmbral dependencies (perhaps, a good idea to spin up a virtualenv before):
    - `pip3 install cryptography`
    - `pip3 install pynacl`
    - Install `libffi` headers (in Debian-based Linux distributions: `apt-get install libffi-dev`)
2. Clone pyUmbral and install it:
    - `git clone https://github.com/nucypher/pyUmbral.git`
    - `pip3 install -e pyUmbral`
3. Copy the `nucypher.py` file from this project to your own.
    - Use as `from nucypher import MockNetwork`
    - The `MockNetwork` object is meant to be instantiated once and used as needed.
    - See the `test.py` file for an example of how it's used.


## API Description:
1. `MockNetwork.grant` -- Creates a mock policy on the mocked network. This will return a string with a `policy_id`. You will use this policy ID to reencrypt and revoke the policy.
2. `MockNetwork.reencrypt` -- Re-encrypts a Capsule `M` times on the mock network. This requires a policy id, a min number of re-encryptions specified during `pre.split_rekey`, and a capsule object. This returns a list of capsule frags for Bob to attach to his capsule and use during `pre.decrypt`.
3. `MockNetwork.revoke` -- Revokes a policy from the network and makes re-encryptions impossible. This makes the `MockNetwork` object delete the stored kfrags stored on it per policy_id.


### Links:
GitHub Links:

https://github.com/nucypher/pyUmbral/

https://github.com/nucypher/umbral-doc/
    
https://github.com/nucypher/nucypher-kms/

Community Links:

https://discord.gg/7rmXa3S 

https://twitter.com/nucypher/

https://nucypher.com/
