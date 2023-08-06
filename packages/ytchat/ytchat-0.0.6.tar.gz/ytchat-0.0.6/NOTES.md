## Data Volume

- Create a new volume
- Attach volume to EC2 instance
- Format an attached volume
  - sudo lsblk -f
  - sudo mkfs -t xfs /dev/xvdf
- Mount a formated volume
  - sudo mount /dev/xvdf /data
- Increase the size of the data volume
- Extend the file system
  - Keep in mind that the file system cannot be extended until the volume enters the optimizing state.
  - df -hT
  - sudo xfs_growfs -d /data
  - df -hT

## Dependencies

Installing collected packages: wcwidth, tokenizers, sentencepiece, pydub, pathtools, mpmath, lit, ffmpy, cmake, appdirs, uc-micro-py, sympy, svgwrite, setproctitle, sentry-sdk, semantic-version, regex, psutil, prompt-toolkit, orjson, nvidia-nvtx-cu11, nvidia-nccl-cu11, nvidia-cusparse-cu11, nvidia-curand-cu11, nvidia-cufft-cu11, nvidia-cuda-runtime-cu11, nvidia-cuda-nvrtc-cu11, nvidia-cuda-cupti-cu11, nvidia-cublas-cu11, networkx, markdown2, kiwisolver, fsspec, fonttools, docker-pycreds, cycler, contourpy, aiofiles, wavedrom, nvidia-cusolver-cu11, nvidia-cudnn-cu11, mdit-py-plugins, matplotlib, linkify-it-py, huggingface-hub, httpcore, wandb, transformers, httpx, gradio, triton, torch, accelerate, fschat
Successfully installed accelerate-0.18.0 aiofiles-23.1.0 appdirs-1.4.4 cmake-3.26.3 contourpy-1.0.7 cycler-0.11.0 docker-pycreds-0.4.0 ffmpy-0.3.0 fonttools-4.39.3 fschat-0.2.1 fsspec-2023.4.0 gradio-3.23.0 httpcore-0.17.0 httpx-0.24.0 huggingface-hub-0.13.4 kiwisolver-1.4.4 linkify-it-py-2.0.0 lit-16.0.1 markdown2-2.4.8 matplotlib-3.7.1 mdit-py-plugins-0.3.3 mpmath-1.3.0 networkx-3.1 nvidia-cublas-cu11-11.10.3.66 nvidia-cuda-cupti-cu11-11.7.101 nvidia-cuda-nvrtc-cu11-11.7.99 nvidia-cuda-runtime-cu11-11.7.99 nvidia-cudnn-cu11-8.5.0.96 nvidia-cufft-cu11-10.9.0.58 nvidia-curand-cu11-10.2.10.91 nvidia-cusolver-cu11-11.4.0.1 nvidia-cusparse-cu11-11.7.4.91 nvidia-nccl-cu11-2.14.3 nvidia-nvtx-cu11-11.7.91 orjson-3.8.10 pathtools-0.1.2 prompt-toolkit-3.0.38 psutil-5.9.4 pydub-0.25.1 regex-2023.3.23 semantic-version-2.10.0 sentencepiece-0.1.98 sentry-sdk-1.19.1 setproctitle-1.3.2 svgwrite-1.4.3 sympy-1.11.1 tokenizers-0.13.3 torch-2.0.0 transformers-4.29.0.dev0 triton-2.0.0 uc-micro-py-1.0.1 wandb-0.14.2 wavedrom-2.0.3.post3 wcwidth-0.2.6

## AWS

- Region: us-east-1
- Name: Python 3.11 on CentOS7.9 with support by Fleximg
- AMI: ami-0cacc31976f5d4e31

Deep Learning AMI GPU PyTorch 2.0.0 (Ubuntu 20.04) 20230401
ami-0996d1ddefe09ff57 (64-bit (x86))
Supported EC2 instances: G3, P3, P3dn, P4d, P4de, G5, G4dn. 
Release notes: https://docs.aws.amazon.com/dlami/latest/devguide/appendix-ami-release-notes.html

Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
ami-0a695f0d95cefc163 (64-bit (x86)) / ami-0af198159897e7a29 (64-bit (Arm))
Ubuntu Server 22.04 LTS (HVM),EBS General Purpose (SSD) Volume Type. Support available from Canonical (http://www.ubuntu.com/cloud/services).

t2.2xlarge
==========
vCPUs: 8
Architecture: x86_64
Memory(GiB): 32

On-Demand Linux pricing: 0.3712 USD per Hour

g3.4xlarge
==========
vCPUs: 16
Architecture: x86_64
Memory(GiB): 122

GPUs: 1
GPU memory (GiB): 8
GPU manufacturer: NVIDIA
GPU name: M60

On-Demand Linux pricing: 1.14 USD per Hour

g3.8xlarge
==========
vCPUs: 32
Architecture: x86_64
Memory(GiB): 244

GPUs: 2
GPU memory (GiB): 8
GPU manufacturer: NVIDIA
GPU name: M60

On-Demand Linux pricing: 2.28 USD per Hour

## make base

- export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

TypeError: Descriptors cannot not be created directly.
If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0.
If you cannot immediately regenerate your protos, some other possible workarounds are:
 1. Downgrade the protobuf package to 3.20.x or lower.
 2. Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python (but this will use pure-Python parsing and will be much slower).

More information: https://developers.google.com/protocol-buffers/docs/news/2022-05-06#python-updates
