#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const command = process.argv[2];
const input = process.argv.slice(3).join(" ").trim();
const cwd = process.cwd();
const configDir = path.join(cwd, ".cognet");
const configPath = path.join(configDir, "config.json");
const legacyConfigPath = path.join(cwd, ".cognet.json");
const defaultApiUrl = "http://localhost:8000/api/v1";
const separator = "────────────────────────";

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
  const candidatePaths = [configPath, legacyConfigPath];

  for (const candidatePath of candidatePaths) {
    if (!fs.existsSync(candidatePath)) {
      continue;
    }

    try {
      return JSON.parse(fs.readFileSync(candidatePath, "utf8"));
    } catch (error) {
      return {};
    }
  }

  return {};
}

function writeConfig(config) {
  fs.mkdirSync(configDir, { recursive: true });
  fs.writeFileSync(configPath, `${JSON.stringify(config, null, 2)}\n`);
}

function resolveConfig(options) {
  const existing = readConfig();
  return {
    apiUrl: options.url || existing.api_url || existing.apiUrl || process.env.COGNET_API_URL || defaultApiUrl,
    token: options.token || existing.token || process.env.COGNET_API_KEY || existing.apiKey || "",
    projectId: existing.project_id || existing.projectId || crypto.randomUUID().slice(0, 8),
  };
}

async function loadUi() {
  try {
    const [chalkModule, boxenModule, oraModule] = await Promise.all([
      import("chalk"),
      import("boxen"),
      import("ora"),
    ]);

    return {
      chalk: chalkModule.default,
      boxen: boxenModule.default,
      ora: oraModule.default,
    };
  } catch (error) {
    const passthrough = (value) => value;
    const dim = (value) => value;
    const gray = (value) => value;
    const white = (value) => value;
    const green = (value) => value;
    const yellow = (value) => value;
    const bold = (value) => value;

    return {
      chalk: { dim, gray, white, green, yellow, bold },
      boxen: (value) => value,
      ora: () => ({ start: () => ({ succeed: passthrough, fail: passthrough, stop: passthrough }) }),
    };
  }
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
  cognet status
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

function normalizeResponse(payload) {
  if (typeof payload === "string") {
    return {
      response: payload,
      next_step: "",
      insight: "",
      reasoning: "",
      temporal_context: "",
      completed: [],
      tasks: [],
    };
  }

  const context = payload?.context || {};

  return {
    response: payload?.response || payload?.final_output || "",
    next_step: payload?.next_step || payload?.decision || payload?.suggestion || "",
    insight: payload?.insight || "",
    reasoning: payload?.reasoning || "",
    temporal_context: payload?.temporal_context || "",
    response_time_ms: payload?.response_time_ms,
    completed: Array.isArray(context?.completed) ? context.completed : [],
    tasks: Array.isArray(context?.tasks) ? context.tasks : [],
    project: context?.project || "",
  };
}

async function renderCard(title, body) {
  const { chalk, boxen } = await loadUi();
  const content = `${chalk.bold(title)}\n${chalk.gray(separator)}\n\n${body}`;
  return boxen(content, {
    padding: 1,
    margin: 0,
    borderStyle: "round",
    borderColor: "gray",
  });
}

async function renderInitOutput(config) {
  const { chalk } = await loadUi();
  const body = [
    `${chalk.green("✔")} Cognet initialized`,
    "",
    "Project linked to Cognet",
    "Tracking started",
    "",
    "Try:",
    `  cognet send ${chalk.dim('"I built API"')}`,
  ].join("\n");

  console.log(await renderCard("Cognet", body));
  console.log(chalk.dim(`Config: ${configPath}`));
}

async function renderConnectOutput(config, healthy) {
  const { chalk } = await loadUi();
  const body = [
    `${healthy ? chalk.green("✔") : chalk.yellow("⚑")} Cognet connected`,
    "",
    `Project: ${config.projectId}`,
    `Backend: ${config.apiUrl}`,
    `Tracking: ${healthy ? "active" : "saved locally"}`,
  ].join("\n");

  console.log(await renderCard("Cognet", body));
}

async function renderSendOutput(message, payload) {
  const { chalk } = await loadUi();
  const data = normalizeResponse(payload);
  const lines = [
    `Recorded:`,
    `${chalk.white(`• ${message}`)}`,
    "",
    `Next Step:`,
    `${chalk.white(data.next_step || "Define your next move")}`,
    "",
    `Insight:`,
    `${chalk.white(data.insight || "You are progressing from backend setup to data flow")}`,
  ];

  console.log(await renderCard("Cognet", lines.join("\n")));
}

async function renderNextOutput(payload) {
  const { chalk } = await loadUi();
  const data = normalizeResponse(payload);
  const lines = [
    `Next Step`,
    "",
    `${chalk.white(data.next_step || "Define your next move")}`,
    "",
    `Tip:`,
    `${chalk.dim(data.insight || "Focus on edge cases")}`,
  ];

  console.log(await renderCard("Next Step", lines.join("\n")));
}

async function renderStatusOutput(payload) {
  const { chalk } = await loadUi();
  const data = normalizeResponse(payload);
  const completedLines = data.completed.length ? data.completed : ["API"];
  const nextLines = data.tasks.length ? data.tasks : [data.next_step || "optimize retrieval"];
  const todayBody = data.temporal_context
    ? data.temporal_context.replace(/^(Today|Yesterday|This Week):\s*/i, "").trim()
    : "• working on retrieval";
  const lines = [
    `Today:`,
    `${chalk.white(todayBody)}`,
    "",
    `Completed:`,
    `${chalk.white(completedLines.map((item) => `• ${item}`).join("\n"))}`,
    "",
    `Next:`,
    `${chalk.white(nextLines.map((item) => `• ${item}`).join("\n"))}`,
  ];

  console.log(await renderCard("Current State", lines.join("\n")));
}

async function run() {
  const options = parseOptions(process.argv.slice(3));
  const config = resolveConfig(options);
  const spinnerEnabled = process.stdout.isTTY;

  if (!command || command === "help" || command === "--help" || command === "-h") {
    printUsage();
    return;
  }

  if (command === "init") {
    writeConfig({
      project_id: config.projectId,
      api_url: config.apiUrl,
      token: config.token || undefined,
    });
    await renderInitOutput(config);
    return;
  }

  if (command === "connect") {
    writeConfig({
      project_id: config.projectId,
      api_url: config.apiUrl,
      token: config.token || undefined,
    });

    try {
      const response = await requestJson(`${config.apiUrl}/health`);
      await renderConnectOutput(config, response.data?.status === "ok");
    } catch (error) {
      await renderConnectOutput(config, false);
    }

    return;
  }

  if (command === "status") {
    if (spinnerEnabled) {
      const { ora } = await loadUi();
      const spinner = ora("Thinking...").start();
      try {
        const payload = await postChat(config.apiUrl, config.token, "what is my status?");
        spinner.succeed("Done");
        await renderStatusOutput(payload);
      } catch (error) {
        spinner.fail("Unable to fetch status");
        throw error;
      }
    } else {
      const payload = await postChat(config.apiUrl, config.token, "what is my status?");
      await renderStatusOutput(payload);
    }

    return;
  }

  if (command === "send") {
    if (!input) {
      throw new Error("Missing message. Example: cognet send \"I built API\"");
    }

    const { ora } = await loadUi();
    const spinner = spinnerEnabled ? ora("Thinking...").start() : null;
    const result = await postChat(config.apiUrl, config.token, input);
    if (spinner) {
      spinner.succeed("Done");
    }
    await renderSendOutput(input, result);
    return;
  }

  if (command === "next") {
    const { ora } = await loadUi();
    const spinner = spinnerEnabled ? ora("Thinking...").start() : null;
    const result = await postChat(config.apiUrl, config.token, "what should I do next?");
    if (spinner) {
      spinner.succeed("Done");
    }
    await renderNextOutput(result);
    return;
  }

  printUsage();
}

run().catch((error) => {
  const message = error?.response?.data?.detail || error.message || String(error);
  console.error(`Cognet CLI error: ${message}`);
  process.exit(1);
});