// Zotero -> Tools -> Developer -> Run JavaScript, with "Run as async function" ticked.
//
// Normalizes four compound surnames that Zotero holds in several broken forms:
// the particle stranded in the First field ("Arnaud Le" | "Boyer"), a duplicated
// name part, a missing space, a U+2010 hyphen and a U+00A0 no-break space.
//
// Back up first: quit Zotero and copy ~/Zotero/zotero.sqlite somewhere safe.
// Leave DRY_RUN = true for the first run; it reports without saving.

const DRY_RUN = true;

// Collapse initials-only records into the full given name as well. These are
// the same people, but it changes rendering ("Naveira Garabato, A." becomes
// "Naveira Garabato, A.C."), so it is off by default.
const NORMALIZE_INITIALS = false;

const FIXES = [
  // --- particle stranded in the First field -------------------------------
  { from: ["Arnaud Le",          "Boyer"],   to: ["Arnaud",     "Le Boyer"] },
  { from: ["Bieito Fernandez",   "Castro"],  to: ["Bieito",     "Fernández-Castro"] },
  { from: ["Bieito Fernández",   "Castro"],  to: ["Bieito",     "Fernández-Castro"] },
  { from: ["A C Naveira",        "Garabato"],to: ["A. C.",      "Naveira Garabato"] },
  { from: ["A. C. Naveira",      "Garabato"],to: ["A. C.",      "Naveira Garabato"] },
  { from: ["A. Naveira",         "Garabato"],to: ["A.",         "Naveira Garabato"] },
  { from: ["Alberto C. Naveira", "Garabato"],to: ["Alberto C.", "Naveira Garabato"] },
  { from: ["Alberto Naveira",    "Garabato"],to: ["Alberto",    "Naveira Garabato"] },
  { from: ["Eva van",            "Haren"],   to: ["Eva",        "van Haren"] },
  { from: ["Hans van",           "Haren"],   to: ["Hans",       "van Haren"] },
  { from: ["Martijn van",        "Haren"],   to: ["Martijn",    "van Haren"] },

  // --- malformed surnames --------------------------------------------------
  { from: ["Arnaud",             "LeBoyer"],           to: ["Arnaud",     "Le Boyer"] },
  { from: ["Bieito",             "Fernández Castro"],  to: ["Bieito",     "Fernández-Castro"] },
  { from: ["Alberto C. Naveira", "Naveira Garabato"],  to: ["Alberto C.", "Naveira Garabato"] },
  { from: ["A. C.",              "Naveira‐Garabato"], to: ["A. C.",  "Naveira Garabato"] },
  { from: ["Alberto C",          "Naveira Garabato"],  to: ["Alberto C.", "Naveira Garabato"] },
  { from: ["Hans",               "Van Haren"],         to: ["Hans",       "van Haren"] },
  { from: ["Hans",               "van Haren"],    to: ["Hans",       "van Haren"] },
];

const INITIAL_FIXES = [
  { from: ["A.",     "Le Boyer"],         to: ["Arnaud",     "Le Boyer"] },
  { from: ["A. C.",  "Naveira Garabato"], to: ["Alberto C.", "Naveira Garabato"] },
  { from: ["Alberto","Naveira Garabato"], to: ["Alberto C.", "Naveira Garabato"] },
  { from: ["A.",     "Naveira Garabato"], to: ["Alberto C.", "Naveira Garabato"] },
  { from: ["H.",     "van Haren"],        to: ["Hans",       "van Haren"] },
];

const rules = NORMALIZE_INITIALS ? FIXES.concat(INITIAL_FIXES) : FIXES;

const search = new Zotero.Search();
search.libraryID = Zotero.Libraries.userLibraryID;
search.addCondition("deleted", "false");
const items = await Zotero.Items.getAsync(await search.search());

let touched = 0;
const log = [];

for (const item of items) {
  if (!item.isRegularItem()) continue;
  const creators = item.getCreators();
  let changed = false;

  for (const c of creators) {
    if (c.fieldMode === 1) continue;          // single-field names are fine
    for (const f of rules) {
      if (c.firstName === f.from[0] && c.lastName === f.from[1]) {
        log.push(`${(item.getField("date") || "????").substr(0, 4)}  `
               + `[${c.firstName}] [${c.lastName}] -> [${f.to[0]}] [${f.to[1]}]  `
               + `${(item.getField("title") || "").substr(0, 55)}`);
        c.firstName = f.to[0];
        c.lastName  = f.to[1];
        changed = true;
      }
    }
  }

  if (changed) {
    touched++;
    if (!DRY_RUN) {
      item.setCreators(creators);
      await item.saveTx();
    }
  }
}

log.sort();
return (DRY_RUN ? "DRY RUN, nothing saved\n" : "SAVED\n")
     + `${touched} items, ${log.length} creator records\n\n`
     + log.join("\n");
