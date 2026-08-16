export const meta = {
  name: 'multiagentelbo-0815-deep-review-wave2',
  description: 'Wave 2: adversarial skeptics attack the contested Critical/High findings, then an evidence-weighted adjudicator assigns verdicts',
  phases: [
    { title: 'Skeptics' },
    { title: 'Adjudicate' },
  ],
}

// args: { contested: [ { id, severity, title, location, one_line_evidence, source_file } ] }
// If args is absent the skeptics are told to read the findings directory and pick the targets
// themselves, so this script is runnable standalone after a rate-limit interruption.

const REPO = 'C:/Users/chris and christine/Desktop/MultiAgentELBO'
const DIR = REPO + '/docs/reviews/2026-08-15-deep-review'
const OUT = DIR + '/findings'
const HEAD = '8ce635807a6ca2a388255fc996c98f7c535e5843'
const MAX_SKEPTICS = 12

const contested = (args && args.contested) || []

const SKEPTIC_BASE = `
You are an adversarial SKEPTIC in a deep review of theory work at "${REPO}" (revision ${HEAD},
branch review/2026-08-15-deep-review). Wave 1 investigators produced findings against work committed
2026-08-15 by another AI agent. Your job is to ATTACK one specific wave-1 finding and determine
whether it survives.

You are not a second opinion. You are trying to KILL the finding. The standard ways a finding of this
kind dies:
  - the investigator misread the document, and the text already says what they demand
  - the hypothesis they say is missing is stated elsewhere in the package (search for it before
    accepting the finding — check the problem contract, the claim ledger, and the notation standard)
  - the claim is correctly fenced in the derivation and only the SUMMARY prose is loose, which
    changes the severity and the location but not the mathematics
  - the severity is inflated: an attribution/novelty issue is not a correctness issue, and a
    presentational looseness is not a proof gap
  - the investigator asserted a counterexample without exhibiting one, or exhibited one that violates
    a stated premise
  - the "standard result" they cite does not actually say what they claim it says — CHECK THE SOURCE

But you must also CONCEDE cleanly when the finding is right. A skeptic who cannot concede is useless.

RULES OF EVIDENCE — identical to wave 1:
  - Reconstruct the disputed mathematics yourself. Do not adjudicate by reading either party's prose.
  - If you assert the finding is wrong, exhibit the passage, the derivation, or the executed command
    with real output that shows it.
  - If you cite a primary source, cite it by author and result, and verify it with WebSearch/WebFetch
    rather than memory.
  - Agreement between you and the investigator is not evidence. Only reconstruction, execution, or a
    primary source is.

PERSISTENCE MANDATE: a rate limit may interrupt this session. Write your file with
"STATUS: IN_PROGRESS" BEFORE substantive work, append as you go, and set "STATUS: COMPLETE" at the
end. The file on disk is the deliverable.

YOUR VERDICT must be exactly one of:
  UPHELD          — the finding stands as stated, at the stated severity
  UPHELD_REDUCED  — a real defect exists but the severity or scope was overstated; state the correct ones
  REFUTED         — the finding is wrong; state the specific passage or derivation that kills it
  INCONCLUSIVE    — you could not settle it; state the one specific check that would settle it

Also state the FALSIFIER OF YOUR OWN ATTACK: the fact that would show your verdict is wrong.
`

const SKEPTIC_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['finding_id', 'verdict', 'corrected_severity', 'rationale', 'evidence_kind', 'file_written'],
  properties: {
    finding_id: { type: 'string' },
    verdict: { type: 'string', enum: ['UPHELD', 'UPHELD_REDUCED', 'REFUTED', 'INCONCLUSIVE'] },
    corrected_severity: { type: 'string', enum: ['Critical', 'High', 'Medium', 'Low', 'None'] },
    rationale: { type: 'string' },
    evidence_kind: {
      type: 'string',
      enum: ['reconstructed_derivation', 'executed_command', 'primary_source', 'document_passage', 'none'],
      description: 'none means the verdict rests on judgment alone and must be treated as INCONCLUSIVE by the adjudicator',
    },
    self_falsifier: { type: 'string' },
    file_written: { type: 'string' },
  },
}

phase('Skeptics')

let targets = contested.slice(0, MAX_SKEPTICS)
if (contested.length > MAX_SKEPTICS) {
  log(`NOTE: ${contested.length} contested findings; dispatching skeptics for the top ${MAX_SKEPTICS} by severity. Dropped: ${contested.slice(MAX_SKEPTICS).map((c) => c.id).join(', ')} — these are recorded as UNCHALLENGED in the report, not as confirmed.`)
}

if (targets.length === 0) {
  log('No contested findings passed in via args — dispatching a single triage skeptic to select targets from the findings directory itself.')
  targets = [{ id: 'SELF-TRIAGE', severity: 'unknown', title: 'select and attack the strongest Critical/High findings on disk', location: OUT, one_line_evidence: '', source_file: OUT }]
}

const verdicts = await parallel(
  targets.map((t, i) => () =>
    agent(
      `${SKEPTIC_BASE}

THE FINDING YOU MUST ATTACK
  id:        ${t.id}
  severity:  ${t.severity}
  title:     ${t.title}
  location:  ${t.location}
  summary:   ${t.one_line_evidence}
  full text: read it in ${t.source_file || OUT} (find the finding block with this title)

${t.id === 'SELF-TRIAGE'
  ? `SPECIAL INSTRUCTION: no specific finding was passed to you. Read every file in ${OUT}, select the
single strongest Critical or High finding that has NOT already been attacked (check for existing
V-*.md files first and skip anything already covered), and attack that one. Name your choice in your
output and write to ${OUT}/V-selftriage-${i + 1}.md.`
  : `Also read ${OUT}/P0-principal-reviewer-notes.md before you start. The principal reviewer
independently reconstructed several of the load-bearing identities and recorded which ones CHECK OUT.
If your assigned finding contradicts one of those reconstructions, say so explicitly and determine
which reconstruction is correct — do not defer to either.

WRITE TO: ${OUT}/V-${t.id}.md`}
`,
      { label: `skeptic:${t.id}`, phase: 'Skeptics', schema: SKEPTIC_SCHEMA }
    ).then((v) => (v ? { ...v, finding: t } : { finding_id: t.id, verdict: 'INCONCLUSIVE', corrected_severity: 'None', rationale: 'skeptic agent died or was skipped — re-dispatch on resume', evidence_kind: 'none', file_written: '', finding: t }))
  )
)

phase('Adjudicate')

const clean = verdicts.filter(Boolean)

const adjudication = await agent(
  `You are the ADJUDICATOR for a deep review of theory work at "${REPO}", revision ${HEAD}.

You assign the final verdict on each contested finding. You do this ONLY from recorded evidence, never
by counting votes and never by weighing how confident either party sounded.

INPUTS — read all of these from disk:
  ${OUT}/P0-principal-reviewer-notes.md   (the principal reviewer's own reconstructions)
  ${OUT}/P*.md                            (the ten wave-1 investigator files)
  ${OUT}/V-*.md                           (the skeptic files)

The skeptics returned these structured verdicts:
${JSON.stringify(clean.map((v) => ({ id: v.finding_id, verdict: v.verdict, severity: v.corrected_severity, evidence_kind: v.evidence_kind, rationale: v.rationale })), null, 2)}

ADJUDICATION RULES — these are binding:
 1. A finding is CONFIRMED only if it rests on a reconstructed derivation, an executed command with
    real output, or a cited primary source. Investigator judgment alone is NOT sufficient, no matter
    how many agents agree. Any verdict whose evidence_kind is "none" is INCONCLUSIVE by construction.
 2. Where a skeptic and an investigator disagree and BOTH cite eligible evidence, you must reconstruct
    the disputed step YOURSELF and say which is right, showing your work. If you cannot, the finding is
    INCONCLUSIVE and you must name the one specific check that would settle it.
 3. The principal reviewer's P0 reconstructions are eligible evidence but are not privileged. If a
    skeptic or investigator refutes one with better evidence, say so plainly.
 4. Severity discipline. Correctness defects and novelty/attribution defects are DIFFERENT things and
    must not be merged. A correct theorem that is a restatement of a classical result is not a
    Critical finding; it is a Medium attribution finding and possibly a High overclaim finding about
    the surrounding certification language. Say which.
 5. Findings dropped from the skeptic pass for budget reasons are UNCHALLENGED, not confirmed. List
    them separately and say so.
 6. Report claims that CHECKED OUT as prominently as defects. This review's most likely honest outcome
    is "the mathematics is largely correct and carefully fenced, but the certification language and the
    novelty claims outrun it" — if that is what the evidence shows, say it in those terms. If the
    evidence shows something worse or something better, say that instead. Do not shade toward drama or
    toward reassurance.

OUTPUT: write ${OUT}/ADJUDICATION.md with STATUS: COMPLETE at the top, containing
  - a verdict table: finding id | investigator severity | skeptic verdict | ADJUDICATED verdict |
    adjudicated severity | evidence relied on
  - your own reconstruction for every case where you overrode a skeptic
  - the unchallenged list
  - a short section "What actually checks out"
Then return the structured summary.`,
  {
    label: 'adjudicator',
    phase: 'Adjudicate',
    effort: 'high',
    schema: {
      type: 'object',
      additionalProperties: false,
      required: ['confirmed', 'refuted', 'inconclusive', 'unchallenged', 'bottom_line'],
      properties: {
        confirmed: {
          type: 'array',
          items: {
            type: 'object',
            additionalProperties: false,
            required: ['id', 'severity', 'title', 'evidence'],
            properties: {
              id: { type: 'string' },
              severity: { type: 'string', enum: ['Critical', 'High', 'Medium', 'Low'] },
              title: { type: 'string' },
              evidence: { type: 'string' },
            },
          },
        },
        refuted: { type: 'array', items: { type: 'string' } },
        inconclusive: { type: 'array', items: { type: 'string' } },
        unchallenged: { type: 'array', items: { type: 'string' } },
        checked_out: { type: 'array', items: { type: 'string' } },
        bottom_line: { type: 'string', description: 'three sentences maximum, no hedging' },
      },
    },
  }
)

return { head: HEAD, skeptic_verdicts: clean, adjudication }
