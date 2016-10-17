# To run on Google Compute Engine:

1. Create instance from client:

gcloud compute instances create docker-instance --image-family gci-stable --image-project google-containers --zone europe-west1-d --machine-type n1-standard-1

2. Set External IP to static.

3. Firewalls: Allow HTTP traffic.

4. SSH into instance (from GCE console).

5. Clone repository:

git clone https://github.com/synbiochem/CodonGenie.git

6. Run start_server script:

bash start_server.sh