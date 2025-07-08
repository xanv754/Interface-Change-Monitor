module.exports = {
  apps: [
    {
      name: "ICM-App",
      script: "npm",
      args: "run start",
      instances: 1,
      exec_mode: "fork",
      cwd: "./presentation/",
      watch: true,
    },
    {
      name: "ICM-Server",
      script: "./.venv/bin/python3",
      args: "-m uvicorn app:app --reload --host 0.0.0.0 --port 8000 --app-dir ./business/api",
      instances: 1,
      exec_mode: "fork",
      watch: true,
    }
  ]
}
