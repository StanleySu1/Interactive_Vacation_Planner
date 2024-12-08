# Interactive Vacation Planner

## Members

- Bowen Shan (bs7)
- Hongjiang Ye (ye36)
- Kelvin Chong (kvchong2)
- Stanley Su (ssu603)

### Set Up Python Environment

```
conda create -n project python=3.12
conda activate project
pip install -r requirements.txt
```

### Install Ollama

Install ollama from [https://ollama.com/](https://ollama.com/) and use quantized llama3.2:3b:

```
ollama pull llama3.2
```

### Set Up Node

Install nvm from [https://github.com/nvm-sh/nvm](https://github.com/nvm-sh/nvm)

```
nvm use 20.16
```

### Build the React Client

```
cd client
npm install
npm run build
```

### Run Python Server
```
./run.sh
```

Visit [http://localhost:8000/](http://localhost:8000/)
