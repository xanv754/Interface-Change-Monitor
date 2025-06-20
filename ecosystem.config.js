module.exports = {
  apps: [
    {
      name: "ICM-App",
      script: "npm",
      args: "run start",
      instances: 1,
      exec_mode: "fork",
      cwd: "./client/",
      watch: true,
    },
    {
      name: "ICM-Server",
      script: "./server/.venv/bin/python3",
      args: "-m uvicorn app:app --reload --host 0.0.0.0 --port 8000 --app-dir ./api/",
      instances: 1,
      exec_mode: "fork",
      cwd: "./server/src",
      watch: true,
    }
  ]
}
