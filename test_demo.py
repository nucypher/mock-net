# 0. Imports
from umbral import pre, keys, config
from umbral.signing import Signer
from nucypher import MockNetwork

# 1. Setup pyUmbral
config.set_default_curve()


# 2. Generate Keys and setup mock network
alice_privkey = keys.UmbralPrivateKey.gen_key()
alice_pubkey = alice_privkey.get_pubkey()

alice_signing_privkey = keys.UmbralPrivateKey.gen_key()
alice_signing_pubkey = alice_signing_privkey.get_pubkey()
alice_signer = Signer(alice_signing_privkey)

bob_privkey = keys.UmbralPrivateKey.gen_key()
bob_pubkey = bob_privkey.get_pubkey()

mock_kms = MockNetwork()

# 3. Encrypt some data
plaintext = b'attack at dawn!'
ciphertext, capsule = pre.encrypt(alice_pubkey, plaintext)

# 4. Perform split-rekey and grant re-encryption policy
alice_kfrags = pre.split_rekey(alice_privkey, alice_signer, bob_pubkey, 10, 20)
assert len(alice_kfrags) == 20

policy_id = mock_kms.grant(alice_kfrags)
assert type(policy_id) == str

# 5. Perform re-encryption request
bob_capsule = capsule
bob_capsule.set_correctness_keys(alice_pubkey, bob_pubkey, alice_signing_pubkey)
bob_cfrags = mock_kms.reencrypt(policy_id, bob_capsule, 10)
assert len(bob_cfrags) == 10

# 6. Simulate capsule handoff, and set the correctness keys.
#  Correctness keys are used to prove that a cfrag is correct and not modified
#  by a proxy node in the network. They must be set to use the `decrypt` and
#  `attach_cfrag` funtions.
for cfrag in bob_cfrags:
    bob_capsule.attach_cfrag(cfrag)

decrypted_data = pre.decrypt(ciphertext, bob_capsule, bob_privkey, alice_signing_pubkey)
assert decrypted_data == plaintext


# 7. Perform revoke request
mock_kms.revoke(policy_id)


# 8. This should throw a `ValueError`.
try:
    mock_kms.reencrypt(policy_id, capsule, 10)
except ValueError:
    print("An Error was thrown indicating the expected response. Tests have run without problem.")
