import { describe, expect, it } from "vitest";
import { groupByDomain, rankCommands } from "./palette";
import type { ActionSpec } from "./types";

const A = (command: string, label: string, domain: string): ActionSpec => ({
  id: command, command, label, domain, method: "GET", path: "/", fields: [],
});

const actions = [
  A("PTSR", "Search patients", "Patients"),
  A("PTRG", "Register patient", "Patients"),
  A("RXDP", "Dispense (FEFO)", "Pharmacy"),
  A("SVAL", "Outbreak alerts", "Surveillance"),
];

describe("rankCommands", () => {
  it("returns everything for an empty query", () => {
    expect(rankCommands("", actions)).toHaveLength(4);
  });

  it("ranks exact/prefix code matches above label matches", () => {
    const r = rankCommands("pt", actions);
    expect(r.map((a) => a.command)).toEqual(["PTSR", "PTRG"]);
  });

  it("matches on label text too", () => {
    const r = rankCommands("dispense", actions);
    expect(r[0].command).toBe("RXDP");
  });

  it("exact code beats prefix", () => {
    const r = rankCommands("ptsr", actions);
    expect(r[0].command).toBe("PTSR");
  });

  it("returns empty when nothing matches", () => {
    expect(rankCommands("zzz", actions)).toEqual([]);
  });
});

describe("groupByDomain", () => {
  it("groups and orders by the domain order", () => {
    const g = groupByDomain(actions);
    expect(g.map(([d]) => d)).toEqual(["Patients", "Pharmacy", "Surveillance"]);
    expect(g[0][1]).toHaveLength(2);
  });
});
