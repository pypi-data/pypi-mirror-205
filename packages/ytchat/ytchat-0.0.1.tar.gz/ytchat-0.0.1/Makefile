REMOTE_IP=nuts.frank5.link

ws-init: ws-git-config ws-clone ws-makefile

ws-git-config:
	ssh trial@$(REMOTE_IP) \
	    "git config --global user.name $(shell git config --get user.name); \
	     git config --global user.email $(shell git config --get user.email); "

ws-clone:
	ssh trial@$(REMOTE_IP) \
	    "cd workspace; \
		 GIT_SSH_COMMAND='ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no' \
		 git clone git@github.com:yantao0527/FastChat.git; "

ws-makefile:
	scp Makefile trial@${REMOTE_IP}:workspace/FastChat

remote:
	ssh trial@${REMOTE_IP}

remote-rm:
	ssh-keygen -f "$(HOME)/.ssh/known_hosts" -R ${REMOTE_IP}

mount-data:
	lsblk -f
	mkdir data
	sudo mount /dev/xvdf data
	df -hT

umount-data:
	sudo umount /dev/xvdf
	rmdir data

install-pip3:
	sudo apt update
	sudo apt install python3-pip
	sudo pip3 install --upgrade pip  # enable PEP 660 support

install-package:
	pip3 install -e .

#### Serve ####

contoller:
	python3 -m fastchat.serve.controller

worker:
	python3 -m fastchat.serve.model_worker --model-path data/vicuna-7b --device cpu

test-message:
	python3 -m fastchat.serve.test_message --model-name vicunna-7b

web-server:
	python3 -m fastchat.serve.gradio_web_server

mem-free:
	free -h

backgroup:
	-mkdir log
	python3 -m fastchat.serve.controller > log/controller.log 2>&1 &
	python3 -m fastchat.serve.model_worker --model-path data/vicuna-7b --device cpu > log/worker.log 2>&1 &

show-process:
	ps -u $(USER) -f | grep "python3 -m"|grep -v "grep"

kill-controller:
	ps -u $(USER) -f | grep "python3 -m fastchat.serve.controller" | grep -v "grep" | awk '{print "kill -9", $$2}' | sh

kill-worker:
	ps -u $(USER) -f | grep "python3 -m fastchat.serve.model_worker" | grep -v "grep" | awk '{print "kill -9", $$2}' | sh

kill-web-server:
	ps -u $(USER) -f | grep "python3 -m fastchat.serve.gradio_web_server" | grep -v "grep" | awk '{print "kill -9", $$2}' | sh

kill-all: kill-web-server kill-worker kill-controller

clean-log:
	rm *.log 2023-*-*-conv.json
	
#### Model ####

base:
	python3 scripts/convert_llama_weights_to_hf.py \
      --input_dir ./data/llama --model_size 7B --output_dir ./data/llama-7b-base

model:
	python3 -m fastchat.model.apply_delta \
      --base ./data/llama-7b-base \
      --target ./data/vicuna-7b \
      --delta lmsys/vicuna-7b-delta-v1.1

scp-data:
	echo "scp data"
	## scp -r data/llama trial@${REMOTE_IP}:workspace/FastChat/data
	## scp -r data/llama-7b trial@${REMOTE_IP}:workspace/FastChat/data
	## scp -r data/scripts trial@${REMOTE_IP}:workspace/FastChat/data
	## scp -r data/vicuna-7b-delta-1.1 trial@${REMOTE_IP}:workspace/FastChat/data

