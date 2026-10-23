import React, { useEffect, useState } from 'react';
import {
  Cpu,
  Database,
  Play,
  CheckCircle,
  AlertTriangle,
  Layers,
  Code,
  Clock,
  Zap,
  ShieldCheck,
  FileText,
  Search,
  Sparkles,
  ArrowRight,
  RefreshCw,
  GitFork,
  Check,
  X
} from 'lucide-react';
import { apiClient } from '../api/client';
import { LoadingState } from '../components/EmptyState';

export const ConceptsLabPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'crud' | 'modeling' | 'aggregation' | 'indexing' | 'validation' | 'relationships'>('crud');

  // -----------------------------------------------------------------
  // TAB A: CRUD State
  // -----------------------------------------------------------------
  const [selectedCrudOp, setSelectedCrudOp] = useState<string>('insertOne');
  const [crudResult, setCrudResult] = useState<any>(null);
  const [crudLoading, setCrudLoading] = useState<boolean>(false);

  const runCrudOperation = async (op: string) => {
    try {
      setCrudLoading(true);
      setSelectedCrudOp(op);
      const res = await apiClient.post('/concepts/crud', { operation: op });
      setCrudResult(res.data?.data || null);
    } catch (e: any) {
      alert(`CRUD execution error: ${e.message}`);
    } finally {
      setCrudLoading(false);
    }
  };

  // -----------------------------------------------------------------
  // TAB B: Modeling State
  // -----------------------------------------------------------------
  const [modelingData, setModelingData] = useState<any>(null);
  const [modelingLoading, setModelingLoading] = useState<boolean>(false);

  const fetchModelingData = async () => {
    try {
      setModelingLoading(true);
      const res = await apiClient.get('/concepts/modeling');
      setModelingData(res.data?.data || null);
    } catch (e) {
      console.error(e);
    } finally {
      setModelingLoading(false);
    }
  };

  // -----------------------------------------------------------------
  // TAB C: Aggregation Playground State
  // -----------------------------------------------------------------
  const [selectedQueryId, setSelectedQueryId] = useState<string>('1');
  const [aggResult, setAggResult] = useState<any>(null);
  const [aggLoading, setAggLoading] = useState<boolean>(false);

  const runAggregationQuery = async (queryId: string) => {
    try {
      setAggLoading(true);
      setSelectedQueryId(queryId);
      const res = await apiClient.post('/concepts/aggregation', { query_id: queryId });
      setAggResult(res.data?.data || null);
    } catch (e: any) {
      alert(`Aggregation execution error: ${e.message}`);
    } finally {
      setAggLoading(false);
    }
  };

  // -----------------------------------------------------------------
  // TAB D: Indexing & Explain State
  // -----------------------------------------------------------------
  const [indexesSummary, setIndexesSummary] = useState<any>(null);
  const [explainScenario, setExplainScenario] = useState<string>('find_by_sku');
  const [explainPlan, setExplainPlan] = useState<any>(null);
  const [explainCollscanPlan, setExplainCollscanPlan] = useState<any>(null);
  const [explainLoading, setExplainLoading] = useState<boolean>(false);

  const fetchIndexes = async () => {
    try {
      const res = await apiClient.get('/concepts/indexes');
      setIndexesSummary(res.data?.data || null);
    } catch (e) {
      console.error(e);
    }
  };

  const runExplainComparison = async (scenario: string) => {
    try {
      setExplainLoading(true);
      setExplainScenario(scenario);
      // Run with index
      const resIndexed = await apiClient.post('/concepts/explain', {
        scenario,
        force_collscan: false,
      });
      // Run with forced collection scan for side-by-side benchmark
      const resCollscan = await apiClient.post('/concepts/explain', {
        scenario,
        force_collscan: true,
      });
      setExplainPlan(resIndexed.data?.data || null);
      setExplainCollscanPlan(resCollscan.data?.data || null);
    } catch (e: any) {
      alert(`Explain error: ${e.message}`);
    } finally {
      setExplainLoading(false);
    }
  };

  // -----------------------------------------------------------------
  // TAB E: Schema Validation State
  // -----------------------------------------------------------------
  const [validationResult, setValidationResult] = useState<any>(null);
  const [validationLoading, setValidationLoading] = useState<boolean>(false);

  const testSchemaValidation = async (testType: 'valid' | 'invalid') => {
    try {
      setValidationLoading(true);
      const res = await apiClient.post('/concepts/validation', {
        test_type: testType,
        item_name: testType === 'valid' ? 'Valid Mechanical Keyboard' : 'Faulty Negative Price Item',
        price: testType === 'valid' ? 89.99 : -45.0,
        stock: 10,
      });
      setValidationResult(res.data?.data || null);
    } catch (e: any) {
      alert(`Validation test error: ${e.message}`);
    } finally {
      setValidationLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    runCrudOperation('insertOne');
    fetchModelingData();
    runAggregationQuery('1');
    fetchIndexes();
    runExplainComparison('find_by_sku');
    testSchemaValidation('valid');
  }, []);

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-navy-900 via-slate-900 to-indigo-950 text-white p-6 rounded-3xl shadow-card border border-slate-800">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-brand-500/20 text-brand-300 text-xs font-semibold border border-brand-400/30 mb-2">
              <Sparkles className="w-3.5 h-3.5 text-brand-400" />
              <span>Academic NoSQL / Viva Demonstration Laboratory</span>
            </div>
            <h2 className="text-2xl font-extrabold tracking-tight">MongoDB Concepts Interactive Lab</h2>
            <p className="text-slate-300 text-xs mt-1 max-w-2xl leading-relaxed">
              Every operation executed here performs real database commands directly against your local MongoDB instance.
              Inspect live driver syntax, execution statistics, query plans, and schema rejections.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold bg-emerald-500/20 text-emerald-300 px-3 py-1.5 rounded-xl border border-emerald-500/30">
              Live Database: shopsphere
            </span>
          </div>
        </div>

        {/* Tab Navigation Navigation */}
        <div className="flex flex-wrap items-center gap-2 mt-6 pt-4 border-t border-slate-800/80">
          {[
            { id: 'crud', label: '1. CRUD Operations', icon: Play },
            { id: 'modeling', label: '2. Embedding vs Referencing', icon: Layers },
            { id: 'aggregation', label: '3. Aggregation Playground', icon: Code },
            { id: 'indexing', label: '4. Indexing & Explain Plans', icon: Zap },
            { id: 'validation', label: '5. Schema Validation', icon: ShieldCheck },
            { id: 'relationships', label: '6. Data Modeling & Joins', icon: GitFork },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all ${
                  isActive
                    ? 'bg-brand-600 text-white shadow-md shadow-brand-600/30 scale-102'
                    : 'bg-slate-800/70 text-slate-300 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* ------------------------------------------------------------- */}
      {/* TAB 1: CRUD OPERATIONS */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'crud' && (
        <div className="space-y-6">
          <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
            <h3 className="text-base font-bold text-slate-900">Isolated CRUD Sandbox (shopsphere_demo)</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Execute core MongoDB CRUD primitives safely. Destructive actions run inside a dedicated demo namespace.
            </p>

            {/* Operation selector buttons */}
            <div className="flex flex-wrap items-center gap-2 mt-4">
              {[
                { op: 'insertOne', label: 'insertOne()', color: 'blue' },
                { op: 'insertMany', label: 'insertMany()', color: 'indigo' },
                { op: 'find', label: 'find()', color: 'emerald' },
                { op: 'updateOne', label: 'updateOne($inc, $set)', color: 'amber' },
                { op: 'updateMany', label: 'updateMany()', color: 'purple' },
                { op: 'deleteOne', label: 'deleteOne()', color: 'rose' },
                { op: 'deleteMany', label: 'deleteMany() [Reset]', color: 'slate' },
              ].map((item) => (
                <button
                  key={item.op}
                  onClick={() => runCrudOperation(item.op)}
                  disabled={crudLoading}
                  className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold transition-all shadow-xs ${
                    selectedCrudOp === item.op
                      ? 'bg-slate-900 text-white ring-2 ring-brand-500'
                      : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>

          {crudLoading ? (
            <LoadingState message="Executing operation in MongoDB..." />
          ) : crudResult ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left: Code & Explanation */}
              <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-mono text-xs font-bold text-brand-600 bg-brand-50 px-2.5 py-1 rounded-md">
                      Method: {crudResult.operation}
                    </span>
                    <span className="flex items-center gap-1 text-xs text-slate-500">
                      <Clock className="w-3.5 h-3.5" />
                      <span>{crudResult.execution_time_ms} ms</span>
                    </span>
                  </div>

                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5">
                    MongoDB Shell / PyMongo Syntax
                  </h4>
                  <div className="p-3 bg-slate-950 text-emerald-400 font-mono text-xs rounded-xl overflow-x-auto leading-relaxed border border-slate-800">
                    <pre>{crudResult.mongo_code}</pre>
                  </div>

                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mt-4 mb-1">
                    Plain-English Viva Explanation
                  </h4>
                  <p className="text-xs text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100 leading-relaxed">
                    {crudResult.explanation}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                  <span>Target Collection: <strong className="text-slate-800">shopsphere_demo</strong></span>
                  <span>Affected Count: <strong className="text-emerald-600">{crudResult.affected_count}</strong></span>
                </div>
              </div>

              {/* Right: Live Database JSON Response */}
              <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                      Actual Database JSON Output
                    </h4>
                    <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                      Live BSON Result
                    </span>
                  </div>
                  <div className="p-3 bg-slate-900 text-slate-200 font-mono text-[11px] rounded-xl overflow-x-auto max-h-80 overflow-y-auto border border-slate-800">
                    <pre>{JSON.stringify(crudResult.result, null, 2)}</pre>
                  </div>
                </div>

                <div className="mt-4 p-3 bg-blue-50/60 border border-blue-100 rounded-xl text-xs text-blue-900">
                  <p className="font-semibold">Why an isolated collection?</p>
                  <p className="text-[11px] text-blue-700 mt-0.5">
                    Academic Viva best practice: destructive operations (like updateMany or deleteMany) are demonstrated safely in a sandbox collection without endangering primary catalogue records.
                  </p>
                </div>
              </div>
            </div>
          ) : null}
        </div>
      )}

      {/* ------------------------------------------------------------- */}
      {/* TAB 2: EMBEDDING VS REFERENCING */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'modeling' && (
        <div className="space-y-6">
          <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
            <h3 className="text-base font-bold text-slate-900">Embedded Documents vs References</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Understanding NoSQL schema design trade-offs through real ShopSphere order &amp; customer documents.
            </p>
          </div>

          {modelingLoading ? (
            <LoadingState message="Extracting schema comparison models..." />
          ) : modelingData ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Embedded Documents Model */}
              <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-base font-bold text-slate-900">Embedded Model (Denormalization)</h4>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                      High Read Speed
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 mb-3">
                    In ShopSphere, <code className="bg-slate-100 px-1 py-0.5 rounded">orders.items</code> and <code className="bg-slate-100 px-1 py-0.5 rounded">orders.shipping_address</code> are stored directly inside the Order document.
                  </p>

                  <div className="space-y-2 mb-4">
                    {modelingData.embedded_model?.embedded_fields?.map((f: any) => (
                      <div key={f.field} className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
                        <p className="font-mono font-bold text-slate-800">{f.field}</p>
                        <p className="text-slate-600 text-[11px] mt-0.5">{f.description}</p>
                        <p className="text-emerald-700 font-medium text-[11px] mt-1">Why: {f.reason}</p>
                      </div>
                    ))}
                  </div>

                  <h5 className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1">
                    Live Sample Document (orders)
                  </h5>
                  <div className="p-3 bg-slate-900 text-emerald-400 font-mono text-[10px] rounded-xl overflow-x-auto max-h-48 overflow-y-auto">
                    <pre>{JSON.stringify(modelingData.embedded_model?.sample_document, null, 2)}</pre>
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 grid grid-cols-2 gap-2 text-xs">
                  <div className="p-2.5 bg-emerald-50 rounded-xl">
                    <p className="font-bold text-emerald-900 text-[11px] mb-1">Advantages</p>
                    <ul className="list-disc list-inside text-[10px] text-emerald-800 space-y-0.5">
                      <li>Zero joins required</li>
                      <li>Single network roundtrip</li>
                      <li>Price snapshot immutability</li>
                    </ul>
                  </div>
                  <div className="p-2.5 bg-amber-50 rounded-xl">
                    <p className="font-bold text-amber-900 text-[11px] mb-1">Trade-offs</p>
                    <ul className="list-disc list-inside text-[10px] text-amber-800 space-y-0.5">
                      <li>Data duplication across docs</li>
                      <li>16MB BSON size limit</li>
                    </ul>
                  </div>
                </div>
              </div>

              {/* Referenced Documents Model */}
              <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-base font-bold text-slate-900">Referenced Model (Normalization)</h4>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-100 text-blue-800">
                      High Scalability
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 mb-3">
                    In ShopSphere, <code className="bg-slate-100 px-1 py-0.5 rounded">orders.customer_id</code> and <code className="bg-slate-100 px-1 py-0.5 rounded">reviews.product_id</code> store only the BSON ObjectId reference.
                  </p>

                  <div className="space-y-2 mb-4">
                    {modelingData.referenced_model?.example_fields?.map((f: any) => (
                      <div key={f.field} className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
                        <div className="flex items-center justify-between font-mono font-bold text-slate-800">
                          <span>{f.field}</span>
                          <span className="text-brand-600">&rarr; {f.references}</span>
                        </div>
                        <p className="text-slate-600 text-[11px] mt-0.5">{f.description}</p>
                      </div>
                    ))}
                  </div>

                  <h5 className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1">
                    Sample Referenced Record (customers)
                  </h5>
                  <div className="p-3 bg-slate-900 text-blue-300 font-mono text-[10px] rounded-xl overflow-x-auto max-h-48 overflow-y-auto">
                    <pre>{JSON.stringify(modelingData.referenced_model?.sample_referenced_customer, null, 2)}</pre>
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 grid grid-cols-2 gap-2 text-xs">
                  <div className="p-2.5 bg-blue-50 rounded-xl">
                    <p className="font-bold text-blue-900 text-[11px] mb-1">Advantages</p>
                    <ul className="list-disc list-inside text-[10px] text-blue-800 space-y-0.5">
                      <li>Single source of truth</li>
                      <li>Customer updates apply universally</li>
                      <li>Unlimited 1-to-many growth</li>
                    </ul>
                  </div>
                  <div className="p-2.5 bg-amber-50 rounded-xl">
                    <p className="font-bold text-amber-900 text-[11px] mb-1">Trade-offs</p>
                    <ul className="list-disc list-inside text-[10px] text-amber-800 space-y-0.5">
                      <li>Requires $lookup joins</li>
                      <li>Multi-query hydration</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          ) : null}
        </div>
      )}

      {/* ------------------------------------------------------------- */}
      {/* TAB 3: AGGREGATION PIPELINE PLAYGROUND */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'aggregation' && (
        <div className="space-y-6">
          <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
            <h3 className="text-base font-bold text-slate-900">Aggregation Pipeline Playground (8 Real Queries)</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Execute complex pipelines featuring $match, $group, $project, $sort, $unwind, $lookup, and $facet.
            </p>

            {/* 8 Query buttons */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2 mt-4">
              {[
                { id: '1', title: '1. Revenue by Category', stages: ['$match', '$unwind', '$lookup', '$group'] },
                { id: '2', title: '2. Monthly Sales Trends', stages: ['$group', '$dateToString', '$sort'] },
                { id: '3', title: '3. Top-Selling Products', stages: ['$unwind', '$group', '$limit'] },
                { id: '4', title: '4. Customer Spend Leaders', stages: ['$group', '$lookup', '$unwind'] },
                { id: '5', title: '5. Status Distribution ($facet)', stages: ['$facet', '$group'] },
                { id: '6', title: '6. Customer-Order Joins', stages: ['$lookup', '$match', '$project'] },
                { id: '7', title: '7. Computed Ratings Join', stages: ['$lookup', '$unwind', '$group'] },
                { id: '8', title: '8. Average Order Value', stages: ['$project', '$group', '$avg'] },
              ].map((q) => (
                <button
                  key={q.id}
                  onClick={() => runAggregationQuery(q.id)}
                  disabled={aggLoading}
                  className={`p-3 rounded-xl text-left transition border ${
                    selectedQueryId === q.id
                      ? 'bg-brand-50 border-brand-500 text-brand-900 shadow-xs'
                      : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  <p className="text-xs font-bold">{q.title}</p>
                  <div className="flex flex-wrap gap-1 mt-1.5">
                    {q.stages.map((st) => (
                      <span key={st} className="text-[9px] font-mono font-semibold px-1.5 py-0.5 rounded bg-white text-slate-600 border border-slate-200">
                        {st}
                      </span>
                    ))}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {aggLoading ? (
            <LoadingState message="Executing pipeline across MongoDB collections..." />
          ) : aggResult ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left: Pipeline Code & Stages */}
              <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-bold text-slate-900">{aggResult.title}</h4>
                    <span className="flex items-center gap-1 text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                      <Clock className="w-3.5 h-3.5" />
                      <span>{aggResult.execution_time_ms} ms</span>
                    </span>
                  </div>

                  <p className="text-xs text-slate-600 mb-3">{aggResult.description}</p>

                  <div className="flex flex-wrap gap-1.5 mb-3">
                    {aggResult.stages_used?.map((stage: string) => (
                      <span
                        key={stage}
                        className="px-2 py-0.5 rounded-md text-[10px] font-mono font-bold bg-indigo-50 text-indigo-700 border border-indigo-200"
                      >
                        {stage}
                      </span>
                    ))}
                  </div>

                  <h5 className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1">
                    Aggregation Pipeline Code
                  </h5>
                  <div className="p-3 bg-slate-950 text-emerald-400 font-mono text-[11px] rounded-xl overflow-x-auto max-h-72 overflow-y-auto border border-slate-800">
                    <pre>{aggResult.pipeline_code}</pre>
                  </div>
                </div>

                <div className="mt-4 p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
                  <p className="font-bold text-slate-800 mb-0.5">Pipeline Mechanics:</p>
                  <p className="text-slate-600 text-[11px] leading-relaxed">{aggResult.explanation}</p>
                </div>
              </div>

              {/* Right: Live Aggregation JSON Output */}
              <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                      Actual Aggregation Result ({aggResult.result?.length || 0} documents)
                    </h4>
                    <span className="text-[10px] font-bold text-brand-700 bg-brand-50 px-2 py-0.5 rounded-full border border-brand-200">
                      Live Output
                    </span>
                  </div>
                  <div className="p-3 bg-slate-900 text-slate-200 font-mono text-[11px] rounded-xl overflow-x-auto max-h-96 overflow-y-auto border border-slate-800">
                    <pre>{JSON.stringify(aggResult.result, null, 2)}</pre>
                  </div>
                </div>

                <div className="mt-4 text-[11px] text-slate-500">
                  Real data pipeline executed with 0 mock values.
                </div>
              </div>
            </div>
          ) : null}
        </div>
      )}

      {/* ------------------------------------------------------------- */}
      {/* TAB 4: INDEXING & QUERY OPTIMIZATION */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'indexing' && (
        <div className="space-y-6">
          <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
            <h3 className="text-base font-bold text-slate-900">Query Optimization &amp; explain("executionStats")</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Compare query execution plans side-by-side: Index Scan (IXSCAN) vs sequential Collection Scan (COLLSCAN).
            </p>

            <div className="flex flex-wrap items-center gap-2 mt-4">
              {[
                { id: 'find_by_sku', label: 'Query 1: Find by SKU (Unique Index)' },
                { id: 'category_price_filter', label: 'Query 2: Category & Price (Compound Index)' },
                { id: 'orders_status_date', label: 'Query 3: Status & Date (Compound Index)' },
              ].map((s) => (
                <button
                  key={s.id}
                  onClick={() => runExplainComparison(s.id)}
                  disabled={explainLoading}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold transition ${
                    explainScenario === s.id
                      ? 'bg-brand-600 text-white shadow-xs'
                      : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                  }`}
                >
                  {s.label}
                </button>
              ))}
            </div>
          </div>

          {explainLoading ? (
            <LoadingState message="Running explain('executionStats') inside MongoDB engine..." />
          ) : explainPlan && explainCollscanPlan ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Card 1: With Index (IXSCAN) */}
              <div className="bg-white p-5 rounded-2xl border-2 border-emerald-200 shadow-subtle">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                    <h4 className="text-base font-bold text-slate-900">Index Scan (IXSCAN)</h4>
                  </div>
                  <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                    Optimized
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs mb-4">
                  <div className="p-3 bg-slate-50 rounded-xl">
                    <p className="text-[10px] text-slate-500 uppercase font-semibold">Stage</p>
                    <p className="font-mono font-bold text-emerald-600 text-sm">{explainPlan.stage}</p>
                  </div>
                  <div className="p-3 bg-slate-50 rounded-xl">
                    <p className="text-[10px] text-slate-500 uppercase font-semibold">Index Applied</p>
                    <p className="font-mono font-bold text-slate-800 text-xs truncate">{explainPlan.index_used || 'B-Tree'}</p>
                  </div>
                  <div className="p-3 bg-slate-50 rounded-xl">
                    <p className="text-[10px] text-slate-500 uppercase font-semibold">Docs Examined</p>
                    <p className="font-mono font-bold text-slate-900 text-sm">{explainPlan.totalDocsExamined}</p>
                  </div>
                  <div className="p-3 bg-slate-50 rounded-xl">
                    <p className="text-[10px] text-slate-500 uppercase font-semibold">Keys Examined</p>
                    <p className="font-mono font-bold text-slate-900 text-sm">{explainPlan.totalKeysExamined}</p>
                  </div>
                </div>

                <div className="p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl text-xs text-emerald-900">
                  <p className="font-bold">Execution Plan Breakdown:</p>
                  <p className="text-[11px] mt-0.5">{explainPlan.explanation}</p>
                </div>
              </div>

              {/* Card 2: Without Index (COLLSCAN) */}
              <div className="bg-white p-5 rounded-2xl border-2 border-rose-200 shadow-subtle">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-rose-500" />
                    <h4 className="text-base font-bold text-slate-900">Collection Scan (COLLSCAN)</h4>
                  </div>
                  <span className="text-xs font-bold text-rose-700 bg-rose-50 px-2.5 py-0.5 rounded-full border border-rose-200">
                    Unoptimized
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs mb-4">
                  <div className="p-3 bg-slate-50 rounded-xl">
                    <p className="text-[10px] text-slate-500 uppercase font-semibold">Stage</p>
                    <p className="font-mono font-bold text-rose-600 text-sm">{explainCollscanPlan.stage}</p>
                  </div>
                  <div className="p-3 bg-slate-50 rounded-xl">
                    <p className="text-[10px] text-slate-500 uppercase font-semibold">Index Applied</p>
                    <p className="font-mono font-bold text-slate-500 text-xs">None (Full Scan)</p>
                  </div>
                  <div className="p-3 bg-slate-50 rounded-xl">
                    <p className="text-[10px] text-slate-500 uppercase font-semibold">Docs Examined</p>
                    <p className="font-mono font-bold text-rose-600 text-sm">{explainCollscanPlan.totalDocsExamined}</p>
                  </div>
                  <div className="p-3 bg-slate-50 rounded-xl">
                    <p className="text-[10px] text-slate-500 uppercase font-semibold">Keys Examined</p>
                    <p className="font-mono font-bold text-slate-500 text-sm">{explainCollscanPlan.totalKeysExamined}</p>
                  </div>
                </div>

                <div className="p-3 bg-rose-50/70 border border-rose-200 rounded-xl text-xs text-rose-900">
                  <p className="font-bold">Execution Plan Breakdown:</p>
                  <p className="text-[11px] mt-0.5">{explainCollscanPlan.explanation}</p>
                </div>
              </div>
            </div>
          ) : null}

          {/* Active Indexes List */}
          <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
            <h4 className="text-sm font-bold text-slate-900 mb-3">Live Active Indexes on Database Collections</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              {indexesSummary &&
                Object.entries(indexesSummary).map(([col, idxs]: [string, any]) => (
                  <div key={col} className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                    <p className="font-bold text-slate-900 mb-1.5 uppercase font-mono text-[11px]">
                      Collection: {col}
                    </p>
                    <div className="space-y-1">
                      {idxs.map((idx: any, i: number) => (
                        <div key={i} className="flex items-center justify-between text-[11px]">
                          <span className="font-mono font-semibold text-slate-700">{idx.name}</span>
                          <span className="text-[10px] text-slate-500">
                            {idx.unique ? (
                              <span className="text-emerald-600 font-bold">Unique</span>
                            ) : (
                              'Standard'
                            )}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
            </div>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------- */}
      {/* TAB 5: SCHEMA VALIDATION */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'validation' && (
        <div className="space-y-6">
          <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
            <h3 className="text-base font-bold text-slate-900">Database-Level Schema Validation ($jsonSchema)</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Observe MongoDB's native JSON Schema validation rejecting invalid writes at the storage engine level.
            </p>

            <div className="flex items-center gap-3 mt-4">
              <button
                onClick={() => testSchemaValidation('valid')}
                disabled={validationLoading}
                className="flex items-center gap-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
              >
                <CheckCircle className="w-4 h-4" />
                <span>Test 1: Valid Insert (Accepted)</span>
              </button>

              <button
                onClick={() => testSchemaValidation('invalid')}
                disabled={validationLoading}
                className="flex items-center gap-1.5 px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
              >
                <AlertTriangle className="w-4 h-4" />
                <span>Test 2: Invalid Insert (Database Rejection)</span>
              </button>
            </div>
          </div>

          {validationLoading ? (
            <LoadingState message="Submitting write to MongoDB collection validator..." />
          ) : validationResult ? (
            <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-subtle space-y-4">
              <div
                className={`p-4 rounded-xl border flex items-center justify-between ${
                  validationResult.accepted
                    ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
                    : 'bg-rose-50 border-rose-200 text-rose-900'
                }`}
              >
                <div className="flex items-center gap-3">
                  {validationResult.accepted ? (
                    <CheckCircle className="w-6 h-6 text-emerald-600 shrink-0" />
                  ) : (
                    <AlertTriangle className="w-6 h-6 text-rose-600 shrink-0" />
                  )}
                  <div>
                    <h4 className="font-bold text-sm">
                      {validationResult.accepted ? 'Document Accepted by MongoDB' : 'Write Rejected by MongoDB Engine'}
                    </h4>
                    <p className="text-xs mt-0.5">{validationResult.status_message}</p>
                  </div>
                </div>
                <span className="text-xs font-mono font-bold uppercase px-2.5 py-1 rounded bg-white border">
                  {validationResult.test_type} test
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div>
                  <h5 className="font-bold text-slate-700 uppercase text-[10px] tracking-wider mb-1">
                    Document Attempted to Insert
                  </h5>
                  <div className="p-3 bg-slate-900 text-slate-200 font-mono text-[11px] rounded-xl overflow-x-auto">
                    <pre>{JSON.stringify(validationResult.document_attempted, null, 2)}</pre>
                  </div>
                </div>

                <div className="flex flex-col justify-between">
                  <div>
                    <h5 className="font-bold text-slate-700 uppercase text-[10px] tracking-wider mb-1">
                      MongoDB Rejection Details
                    </h5>
                    <div className="p-3 bg-slate-100 rounded-xl text-[11px] font-mono text-slate-800 border">
                      {validationResult.mongodb_error || 'No database error (Rule satisfied: minimum price >= 1.0)'}
                    </div>
                  </div>

                  <div className="mt-4 p-3.5 bg-brand-50 border border-brand-200 rounded-xl text-xs text-brand-900">
                    <p className="font-bold mb-1">Pydantic vs. MongoDB Schema Validation:</p>
                    <p className="text-[11px] text-brand-800 leading-relaxed">
                      {validationResult.explanation}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ) : null}
        </div>
      )}

      {/* ------------------------------------------------------------- */}
      {/* TAB 6: DATA MODELING & JOINS */}
      {/* ------------------------------------------------------------- */}
      {activeTab === 'relationships' && (
        <div className="space-y-6">
          <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
            <h3 className="text-base font-bold text-slate-900">NoSQL Relationships &amp; Joins in Practice</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              How ShopSphere models 1-to-1, 1-to-many, and many-to-many relationships in a document store.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
            {/* 1:1 */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800">1:1 Relationship</span>
                <h4 className="font-bold text-slate-900 text-sm mt-2">Order &rarr; Shipping Address</h4>
                <p className="text-slate-600 mt-1">
                  Modeled as an <strong>embedded sub-document</strong> inside <code className="bg-slate-100 px-1">orders</code>.
                </p>
                <div className="p-2.5 bg-slate-50 rounded-xl border mt-3 font-mono text-[10px]">
                  &#123; street: "...", city: "..." &#125;
                </div>
              </div>
              <p className="text-[11px] text-slate-500 mt-3 pt-2 border-t">
                High cohesion. A shipping address belongs uniquely to one specific order.
              </p>
            </div>

            {/* 1:N */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800">1:N Relationship</span>
                <h4 className="font-bold text-slate-900 text-sm mt-2">Customer &rarr; Orders</h4>
                <p className="text-slate-600 mt-1">
                  Modeled via <strong>ObjectId referencing</strong> (<code className="bg-slate-100 px-1">orders.customer_id</code>).
                </p>
                <div className="p-2.5 bg-slate-50 rounded-xl border mt-3 font-mono text-[10px]">
                  customer_id: ObjectId("...")
                </div>
              </div>
              <p className="text-[11px] text-slate-500 mt-3 pt-2 border-t">
                Prevents order arrays from exceeding MongoDB's 16MB document size limit as customer histories grow.
              </p>
            </div>

            {/* N:M */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-purple-100 text-purple-800">N:M Relationship</span>
                <h4 className="font-bold text-slate-900 text-sm mt-2">Products &rarr; Orders</h4>
                <p className="text-slate-600 mt-1">
                  Modeled via <strong>embedded array of snapshot objects</strong> with product ObjectId references.
                </p>
                <div className="p-2.5 bg-slate-50 rounded-xl border mt-3 font-mono text-[10px]">
                  items: [&#123; product_id, sku, price, qty &#125;]
                </div>
              </div>
              <p className="text-[11px] text-slate-500 mt-3 pt-2 border-t">
                Preserves historical order pricing integrity even if product catalogue prices change later.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
