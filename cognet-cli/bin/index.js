#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");

const command = process.argv[2];
const input = process.argv.slice(3).join(" ").trim();
const cwd = process.cwd();
const configPath = path.join(cwd, ".cognet.json");
const defaultApiUrl = "http://localhost:8000/api/v1";

function parseOptions(args) {
  const options = {};

  for (let index = 0; index < args.length; index += 1) {
    const value = args[index];

    if (value === "--url" && args[index + 1]) {
      options.url = args[index + 1];
      index += 1;
      continue;
    }

    if (value === "--token" && args[index + 1]) {
      options.token = args[index + 1];
      index += 1;
      continue;
    }
  }

  return options;
}

function readConfig() {
  if (!fs.existsSync(configPath)) {
    return {};
  }

  try {
    return JSON.parse(fs.readFileSync(configPath, "utf8"));
  } catch (error) {
    return {};
  }
}

function writeConfig(config) {
  fs.writeFileSync(configPath, `${JSON.stringify(config, null, 2)}\n`);
}

function resolveConfig(options) {
  const existing = readConfig();
  return {
    apiUrl: options.url || existing.apiUrl || process.env.COGNET_API_URL || defaultApiUrl,
    token: options.token || existing.token || process.env.COGNET_API_KEY || existing.apiKey || "",
  };
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const text = await response.text();
  const body = text ? JSON.parse(text) : {};

  if (!response.ok) {
    const detail = body?.detail || body?.message || response.statusText;
    throw new Error(detail);
  }

  return body;
}

function printUsage() {
  console.log(`Cognet CLI

Usage:
  cognet init [--url <api-url>] [--token <api-token>]
  cognet connect [--url <api-url>] [--token <api-token>]
  cognet send "message"
  cognet next
`);
}

async function postChat(apiUrl, token, message) {
  const body = await requestJson(`${apiUrl}/chat`, {
    method: "POST",
    body: JSON.stringify({ message }),
    headers: token
      ? {
          Authorization: `Bearer ${token}`,
        }
      : {},
  });

  return body.data?.response || body.response || body.data || body;
}

async function run() {
  const options = parseOptions(process.argv.slice(3));
  const config = resolveConfig(options);

  if (!command || command === "help" || command === "--help" || command === "-h") {
    printUsage();
    return;
  }

  if (command === "init") {
    writeConfig(config);
    console.log(`Cognet configured at ${configPath}`);
    return;
  }

  if (command === "connect") {
    writeConfig(config);

    try {
      const response = await requestJson(`${config.apiUrl}/health`);
      console.log("Cognet connected.");
      console.log(`Backend: ${config.apiUrl}`);
      console.log(`Status: ${response.data?.status || "ok"}`);
    } catch (error) {
      console.log("Cognet connection saved.");
      console.log(`Backend: ${config.apiUrl}`);
    }

    return;
  }

  if (command === "send") {
    if (!input) {
      throw new Error("Missing message. Example: cognet send \"I built API\"");
    }

    const result = await postChat(config.apiUrl, config.token, input);
    console.log("\nCognet:");
    console.log(result);
    return;
  }

  if (command === "next") {
    const result = await postChat(config.apiUrl, config.token, "what should I do next?");
    console.log("\nNext Step:");
    console.log(result);
    return;
  }

  printUsage();
}

run().catch((error) => {
  const message = error?.response?.data?.detail || error.message || String(error);
  console.error(`Cognet CLI error: ${message}`);
  process.exit(1);
});