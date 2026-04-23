#!/usr/bin/env tsx
/**
 * Brave Instagram Lead Search
 * Fast lead generation using Brave Search API
 * Target: 100+ leads per run, no duplicates
 */

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ============================================
// CONFIGURATION
// ============================================

const CONFIG = {
  DEFAULT_TARGET: 100,
  RESULTS_PER_SEARCH: 20,
  DELAY_BETWEEN_SEARCHES: 2,
  MASTER_CSV_PATH: '/Users/kokayi/.openclaw/workspace/leads/instagram-leads-master.csv',
};

// ============================================
// SEARCH TERMS (Insurance Focus)
// ============================================

const SEARCH_TERMS = [
  // Core insurance (always good)
  'site:instagram.com insurance agent',
  'site:instagram.com licensed insurance agent',
  'site:instagram.com insurance broker',
  'site:instagram.com insurance advisor',
  
  // Life insurance variants
  'site:instagram.com life insurance advisor',
  'site:instagram.com life insurance specialist',
  'site:instagram.com life insurance consultant',
  'site:instagram.com insurance producer',
  
  // Final expense (high intent)
  'site:instagram.com final expense specialist',
  'site:instagram.com final expense advisor',
  'site:instagram.com burial insurance specialist',
  
  // IUL / Indexed products
  'site:instagram.com iul specialist',
  'site:instagram.com indexed life agent',
  'site:instagram.com cash value life insurance',
  
  // Medicare variants
  'site:instagram.com medicare specialist',
  'site:instagram.com medicare advisor',
  'site:instagram.com medicare insurance agent',
  
  // Top Carriers (agents post about these)
  'site:instagram.com "foresters financial" agent',
  'site:instagram.com royal neighbors agent',
  'site:instagram.com "american amicable" agent',
  'site:instagram.com "catholic financial life" agent',
  'site:instagram.com gerber life agent',
  'site:instagram.com ethos life agent',
  'site:instagram.com bestow agent',
  'site:instagram.com ladder life agent',
  'site:instagram.com haven life agent',
  'site:instagram.com banner life agent',
  
  // IMO/FMO partners
  'site:instagram.com family first life',
  'site:instagram.com efinancial agent',
  'site:instagram.com synergy agent',
  'site:instagram.com brightway insurance',
  'site:instagram.com heritage insurance',
  
  // Niche specialties
  'site:instagram.com preneed insurance',
  'site:instagram.com funeral expense agent',
  'site:instagram.com estate planning insurance',
  'site:instagram.com tax free retirement',
  'site:instagram.com living benefits agent',
  'site:instagram.com chronic illness rider',
  
  // Titles/roles
  'site:instagram.com insurance wholesaler',
  'site:instagram.com field underwriting agent',
  'site:instagram.com insurance upline',
  'site:instagram.com agency manager insurance',
  
  // States - Group 1 (south/midwest)
  'site:instagram.com insurance agent mississippi',
  'site:instagram.com insurance agent wisconsin',
  'site:instagram.com insurance agent minnesota',
  'site:instagram.com insurance agent iowa',
  'site:instagram.com insurance agent kansas',
  'site:instagram.com insurance agent nebraska',
  'site:instagram.com insurance agent new mexico',
  'site:instagram.com insurance agent utah',
  'site:instagram.com insurance agent idaho',
  'site:instagram.com insurance agent montana',
  
  // States - Group 2 (northeast/west)
  'site:instagram.com insurance agent maine',
  'site:instagram.com insurance agent vermont',
  'site:instagram.com insurance agent new hampshire',
  'site:instagram.com insurance agent rhode island',
  'site:instagram.com insurance agent delaware',
  'site:instagram.com insurance agent west virginia',
  'site:instagram.com insurance agent hawaii',
  'site:instagram.com insurance agent alaska',
  'site:instagram.com insurance agent wyoming',
  'site:instagram.com insurance agent south dakota',
  'site:instagram.com insurance agent north dakota',
];

// ============================================
// DATABASE SETUP
// ============================================

let db: any;
let leads: any;

async function initDb() {
  if (!db) {
    const dbModule = await import('/Users/kokayi/.openclaw/workspace/db/db.js');
    const schemaModule = await import('/Users/kokayi/.openclaw/workspace/db/schema.js');
    db = dbModule.db;
    leads = schemaModule.leads;
  }
  return { db, leads };
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function sleep(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function createHash(source: string, externalId: string): string {
  return crypto
    .createHash('md5')
    .update(`${source}:${externalId}`.toLowerCase())
    .digest('hex');
}

function shuffle<T>(array: T[]): T[] {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

function extractUsername(url: string): string | null {
  const match = url.match(/instagram\.com\/([^\/\?]+)/);
  return match ? match[1].toLowerCase() : null;
}

function extractFollowers(text: string): number | null {
  const match = text.match(/([\d,]+)\s*(?:followers|Followers)/);
  if (match) {
    return parseInt(match[1].replace(/,/g, ''));
  }
  const kmMatch = text.match(/([\d.]+)\s*([KM])\s*(?:followers|Followers)/i);
  if (kmMatch) {
    const num = parseFloat(kmMatch[1]);
    const multiplier = kmMatch[2].toUpperCase() === 'M' ? 1000000 : 1000;
    return Math.floor(num * multiplier);
  }
  return null;
}

function isInsuranceAgentProfile(text: string, title: string): boolean {
  const lower = (text + ' ' + title).toLowerCase();
  const indicators = [
    'insurance agent', 'insurance broker', 'life insurance',
    'final expense', 'health insurance', 'licensed agent',
    'state farm', 'allstate', 'farmers insurance',
    'new york life', 'northwestern mutual', 'prudential',
    'liberty mutual', 'aflac', 'mutual of omaha',
    'medicare', 'burial insurance', 'annuity',
    'insurance sales', 'insurance professional'
  ];
  return indicators.some(i => lower.includes(i));
}

function isCorporateAccount(username: string): boolean {
  const corporate = [
    'statefarm', 'allstate', 'progressive', 'farmers', 
    'libertymutual', 'nationwide', 'geico', 'aflac',
    'newyorklife', 'prudential', 'metlife', 'guardianlife',
    'northwesternmutual', 'massmutual', 'primerica',
    'p', 'reel', 'stories', 'explore', 'accounts', 'about', 'help'
  ];
  return corporate.includes(username.toLowerCase());
}

// ============================================
// DATABASE OPERATIONS
// ============================================

async function getExistingUsernames(): Promise<Set<string>> {
  const { db, leads } = await initDb();
  const existing = await db.query.leads.findMany({
    where: (leads: any, { eq }: any) => eq(leads.source, 'instagram'),
    columns: { externalId: true }
  });
  return new Set(existing.map((l: any) => l.externalId?.toLowerCase()).filter(Boolean));
}

async function saveToDatabase(leadsData: any[], batchId: string): Promise<any[]> {
  const { db, leads } = await initDb();
  const saved = [];
  
  for (const lead of leadsData) {
    try {
      const hash = createHash('instagram', lead.username);
      
      await db.insert(leads).values({
        source: 'instagram',
        batchId: batchId,
        externalId: lead.username,
        externalUrl: lead.profileUrl,
        fullName: lead.fullName,
        bio: lead.bio,
        followers: lead.followers,
        location: lead.location,
        leadType: 'agent',
        niche: lead.niche || 'general',
        scrapedDate: lead.scrapedDate,
        hash: hash,
        status: 'new',
        metadata: JSON.stringify(lead.metadata || {})
      });
      
      saved.push(lead);
    } catch (e: any) {
      if (!e.message?.includes('UNIQUE constraint')) {
        console.error(`  ✗ error saving ${lead.username}:`, e.message);
      }
    }
  }
  
  return saved;
}

async function getDatabaseStats() {
  const { db } = await initDb();
  const stats = db.$client.prepare(`
    SELECT source, COUNT(*) as count 
    FROM leads 
    GROUP BY source
  `).all();
  
  const total = db.$client.prepare('SELECT COUNT(*) as count FROM leads').get();
  
  return { stats, total: total.count };
}

// ============================================
// BRAVE SEARCH
// ============================================

interface SearchResult {
  url: string;
  title: string;
  description: string;
}

async function searchBrave(query: string, count: number = CONFIG.RESULTS_PER_SEARCH): Promise<SearchResult[]> {
  try {
    const configPath = '/Users/kokayi/.openclaw/openclaw.json';
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const apiKey = config.tools?.web?.search?.apiKey;
    
    if (!apiKey) {
      throw new Error('Brave API key not found in config');
    }
    
    const url = new URL('https://api.search.brave.com/res/v1/web/search');
    url.searchParams.set('q', query);
    url.searchParams.set('count', Math.min(count, 20).toString());
    url.searchParams.set('offset', '0');
    url.searchParams.set('mkt', 'en-US');
    
    const response = await fetch(url.toString(), {
      headers: {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'X-Subscription-Token': apiKey
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    return (data.web?.results || []).map((r: any) => ({
      url: r.url,
      title: r.title,
      description: r.description
    }));
  } catch (e: any) {
    console.error(`  ⚠️ Brave search failed:`, e.message);
    return [];
  }
}

// ============================================
// LEAD EXTRACTION
// ============================================

interface Lead {
  username: string;
  profileUrl: string;
  fullName: string | null;
  bio: string | null;
  followers: number | null;
  location: string | null;
  scrapedDate: string;
  niche: string;
  metadata: any;
}

function extractLeadsFromResults(results: SearchResult[], existingUsernames: Set<string>): Lead[] {
  const newLeads: Lead[] = [];
  
  for (const result of results) {
    const url = result.url;
    if (!url || !url.includes('instagram.com')) continue;
    
    const username = extractUsername(url);
    if (!username) continue;
    
    if (existingUsernames.has(username)) continue;
    if (isCorporateAccount(username)) continue;
    if (username.includes('/') || username.includes('?') || username.length < 2) continue;
    
    const text = `${result.title || ''} ${result.description || ''}`;
    if (!isInsuranceAgentProfile(text, result.title || '')) continue;
    
    let niche = 'general';
    const lowerText = text.toLowerCase();
    if (lowerText.includes('final expense') || lowerText.includes('burial')) {
      niche = 'final_expense';
    } else if (lowerText.includes('medicare')) {
      niche = 'medicare';
    } else if (lowerText.includes('life insurance')) {
      niche = 'life_insurance';
    } else if (lowerText.includes('health insurance')) {
      niche = 'health_insurance';
    }
    
    const lead: Lead = {
      username,
      profileUrl: `https://instagram.com/${username}`,
      fullName: result.title?.split('•')[0]?.trim() || null,
      bio: result.description || null,
      followers: extractFollowers(text),
      location: null,
      scrapedDate: new Date().toISOString().split('T')[0],
      niche,
      metadata: { sourceTitle: result.title }
    };
    
    newLeads.push(lead);
    existingUsernames.add(username);
  }
  
  return newLeads;
}

// ============================================
// MASTER CSV
// ============================================

function appendToMasterCSV(leadsData: Lead[]): string {
  const leadsDir = path.dirname(CONFIG.MASTER_CSV_PATH);
  if (!fs.existsSync(leadsDir)) {
    fs.mkdirSync(leadsDir, { recursive: true });
  }
  
  const headers = ['username', 'profile_url', 'full_name', 'bio', 'followers', 'location', 'niche', 'scraped_date'];
  const fileExists = fs.existsSync(CONFIG.MASTER_CSV_PATH);
  
  const lines = leadsData.map(l => [
    l.username,
    l.profileUrl,
    `"${(l.fullName || '').replace(/"/g, '""')}"`,
    `"${(l.bio || '').replace(/"/g, '""')}"`,
    l.followers || '',
    l.location || '',
    l.niche,
    l.scrapedDate
  ].join(','));
  
  // Write headers only if file doesn't exist
  if (!fileExists) {
    fs.writeFileSync(CONFIG.MASTER_CSV_PATH, headers.join(',') + '\n');
  }
  
  // Append leads
  fs.appendFileSync(CONFIG.MASTER_CSV_PATH, lines.join('\n') + '\n');
  
  return CONFIG.MASTER_CSV_PATH;
}

// ============================================
// MAIN FUNCTION
// ============================================

export async function braveInstagramSearch(
  targetCount: number = CONFIG.DEFAULT_TARGET,
  options: { saveCsv?: boolean } = {}
): Promise<{
  leadsFound: number;
  leadsSaved: number;
  searchesRun: number;
  csvFile: string | null;
  duration: number;
}> {
  
  const startTime = Date.now();
  const runId = `brave-${Date.now()}`;
  
  console.log(`\n🔥 BRAVE INSTAGRAM LEAD SEARCH`);
  console.log(`   Target: ${targetCount} leads`);
  console.log(`   Run ID: ${runId}\n`);
  
  const existingUsernames = await getExistingUsernames();
  console.log(`📊 Existing Instagram leads in DB: ${existingUsernames.size}`);
  
  const searchTerms = shuffle([...SEARCH_TERMS]);
  const allNewLeads: Lead[] = [];
  let searchesRun = 0;
  let consecutiveEmpty = 0;
  const MAX_EMPTY = 5;
  
  for (const term of searchTerms) {
    if (allNewLeads.length >= targetCount) break;
    if (consecutiveEmpty >= MAX_EMPTY) {
      console.log(`\n⚠️ Stopping: ${MAX_EMPTY} consecutive empty searches`);
      break;
    }
    
    console.log(`\n🔎 [${searchesRun + 1}] ${term}`);
    searchesRun++;
    
    try {
      const results = await searchBrave(term);
      
      if (results.length === 0) {
        consecutiveEmpty++;
        console.log(`  ⚠️ No results`);
      } else {
        const newLeads = extractLeadsFromResults(results, existingUsernames);
        
        if (newLeads.length === 0) {
          consecutiveEmpty++;
          console.log(`  • No new leads (${results.length} results checked)`);
        } else {
          consecutiveEmpty = 0;
          console.log(`  ✓ Found ${newLeads.length} new leads`);
          allNewLeads.push(...newLeads);
          
          if (allNewLeads.length >= targetCount * 0.25 && allNewLeads.length % 10 === 0) {
            console.log(`  📈 Progress: ${allNewLeads.length}/${targetCount}`);
          }
        }
      }
    } catch (e: any) {
      console.error(`  ✗ Error:`, e.message);
    }
    
    if (allNewLeads.length < targetCount) {
      await sleep(CONFIG.DELAY_BETWEEN_SEARCHES * 1000);
    }
  }
  
  // Save to database
  console.log(`\n💾 Saving ${allNewLeads.length} leads to database...`);
  const batchId = `brave-${new Date().toISOString().split('T')[0]}-${runId}`;
  const saved = await saveToDatabase(allNewLeads, batchId);
  
  // Save to master CSV
  let csvFile: string | null = null;
  if (saved.length > 0 && options.saveCsv !== false) {
    csvFile = appendToMasterCSV(saved);
    console.log(`  📁 Master CSV: ${csvFile}`);
  }
  
  const { stats, total } = await getDatabaseStats();
  const duration = Math.round((Date.now() - startTime) / 1000);
  
  console.log(`\n✅ COMPLETE`);
  console.log(`   Duration: ${Math.floor(duration / 60)}m ${duration % 60}s`);
  console.log(`   Searches: ${searchesRun}`);
  console.log(`   Leads Found: ${allNewLeads.length}`);
  console.log(`   Leads Saved: ${saved.length}`);
  console.log(`\n📊 DATABASE TOTALS:`);
  stats.forEach((s: any) => console.log(`   - ${s.source}: ${s.count}`));
  console.log(`   - TOTAL: ${total}`);
  
  return {
    leadsFound: allNewLeads.length,
    leadsSaved: saved.length,
    searchesRun,
    csvFile,
    duration
  };
}

// ============================================
// CLI
// ============================================

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const target = parseInt(process.argv[2]) || CONFIG.DEFAULT_TARGET;
  const noCsv = process.argv.includes('--no-csv');
  
  braveInstagramSearch(target, {
    saveCsv: !noCsv
  }).catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
  });
}
