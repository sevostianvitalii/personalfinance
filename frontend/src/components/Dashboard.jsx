import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, PieChart, Pie, Cell } from 'recharts'
import { Download, Tag } from 'lucide-react'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d', '#ffc658', '#ff7300'];

const Dashboard = () => {
    const [period, setPeriod] = useState('Month')
    const [startDate, setStartDate] = useState('')
    const [endDate, setEndDate] = useState('')
    const [category, setCategory] = useState('')
    const [search, setSearch] = useState('')

    const [categoriesList, setCategoriesList] = useState([])
    const [data, setData] = useState([]) // Summary data
    const [breakdown, setBreakdown] = useState([]) // Category data

    const [loading, setLoading] = useState(false)
    const [categorizing, setCategorizing] = useState(false)

    // Fetch unique categories on mount
    useEffect(() => {
        fetch('http://localhost:8000/categories')
            .then(res => res.json())
            .then(data => setCategoriesList(data))
            .catch(err => console.error("Failed to load categories", err))
    }, [])

    const fetchData = async () => {
        setLoading(true)
        try {
            let url = `http://localhost:8000/analysis?period=${period}`
            if (startDate) url += `&start_date=${startDate}`
            if (endDate) url += `&end_date=${endDate}`
            if (category && category !== 'All') url += `&category=${encodeURIComponent(category)}`
            if (search) url += `&search=${encodeURIComponent(search)}`

            const response = await fetch(url)
            if (response.ok) {
                const result = await response.json()
                // result is now { summary: [], breakdown: [] }
                if (Array.isArray(result)) {
                    setData(result)
                    setBreakdown([])
                } else {
                    setData(result.summary || [])
                    setBreakdown(result.breakdown || [])
                }
            }
        } catch (e) {
            console.error("Failed to fetch data", e)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchData()
    }, [period, startDate, endDate, category, search])

    const handleRecategorize = async () => {
        setCategorizing(true)
        try {
            await fetch('http://localhost:8000/categorize', { method: 'POST' })
            fetchData()
            // Reload categories in case new ones appeared
            fetch('http://localhost:8000/categories')
                .then(res => res.json())
                .then(data => setCategoriesList(data))
        } catch (e) {
            console.error("Failed to categorize", e)
        } finally {
            setCategorizing(false)
        }
    }

    const handleDownloadReport = async () => {
        try {
            let url = `http://localhost:8000/report?period=${period}`
            if (startDate) url += `&start_date=${startDate}`
            if (endDate) url += `&end_date=${endDate}`
            if (category && category !== 'All') url += `&category=${encodeURIComponent(category)}`
            if (search) url += `&search=${encodeURIComponent(search)}`

            const response = await fetch(url)
            if (response.ok) {
                const blob = await response.blob()
                const urlObj = window.URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = urlObj
                a.download = `report_${period}.pdf`
                document.body.appendChild(a)
                a.click()
                a.remove()
            }
        } catch (e) {
            console.error("Report download failed", e)
        }
    }

    const totals = data.reduce((acc, curr) => ({
        income: acc.income + curr.income,
        expenses: acc.expenses + curr.expenses,
        net: acc.net + curr.net
    }), { income: 0, expenses: 0, net: 0 })

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '1rem' }}>
                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                    {['Day', 'Week', 'Month', 'Year'].map(p => (
                        <button
                            key={p}
                            className={`btn ${period === p ? 'btn-primary' : 'btn-outline'}`}
                            onClick={() => setPeriod(p)}
                        >
                            {p}
                        </button>
                    ))}
                    <div style={{ width: '1px', height: '2rem', background: 'rgba(255,255,255,0.1)', margin: '0 0.5rem' }}></div>

                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                        <input
                            type="date"
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                            style={{ width: 'auto', padding: '0.5rem' }}
                        />
                        <span style={{ color: 'var(--text-secondary)' }}>to</span>
                        <input
                            type="date"
                            value={endDate}
                            onChange={(e) => setEndDate(e.target.value)}
                            style={{ width: 'auto', padding: '0.5rem' }}
                        />
                    </div>
                </div>

                <div style={{ display: 'flex', gap: '1rem' }}>
                    <button className="btn btn-outline" onClick={handleRecategorize} disabled={categorizing} style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                        <Tag size={18} /> {categorizing ? 'Processing...' : 'Auto Categorize'}
                    </button>
                    <button className="btn btn-outline" onClick={handleDownloadReport} style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                        <Download size={18} /> Export PDF
                    </button>
                </div>
            </div>

            {/* Toolbar Row 2: Filters */}
            <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
                <select
                    value={category}
                    onChange={e => setCategory(e.target.value)}
                    style={{ height: '42px', padding: '0 1rem', borderRadius: '0.5rem', background: 'rgba(15, 23, 42, 0.6)', border: '1px solid rgba(255,255,255,0.1)', color: 'white' }}
                >
                    <option value="">All Categories</option>
                    {categoriesList.map(c => (
                        <option key={c} value={c}>{c}</option>
                    ))}
                </select>

                <input
                    type="text"
                    placeholder="Search description..."
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                    style={{ width: '300px', height: '42px' }}
                />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <h3>Total Income</h3>
                    <p style={{ fontSize: '1.8rem', color: 'var(--success)' }}>+{totals.income.toFixed(2)}</p>
                </div>
                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <h3>Total Expenses</h3>
                    <p style={{ fontSize: '1.8rem', color: 'var(--danger)' }}>{totals.expenses.toFixed(2)}</p>
                </div>
                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <h3>Net Balance</h3>
                    <p style={{ fontSize: '1.8rem', color: totals.net >= 0 ? 'var(--text-primary)' : 'var(--danger)' }}>
                        {totals.net.toFixed(2)}
                    </p>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.5rem' }}>
                <div className="glass-panel" style={{ padding: '2rem', height: '400px' }}>
                    <h3 style={{ marginBottom: '2rem' }}>Financial Overview</h3>
                    {loading ? (
                        <p>Loading chart...</p>
                    ) : (
                        <div style={{ width: '100%', height: '280px' }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={data}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                    <XAxis dataKey="date" stroke="var(--text-secondary)" />
                                    <YAxis stroke="var(--text-secondary)" />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: 'var(--bg-secondary)', borderColor: 'rgba(255,255,255,0.1)' }}
                                        itemStyle={{ color: 'var(--text-primary)' }}
                                    />
                                    <Legend />
                                    <Bar dataKey="income" fill="var(--success)" name="Income" radius={[4, 4, 0, 0]} />
                                    <Bar dataKey="expenses" fill="var(--danger)" name="Expenses" radius={[4, 4, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    )}
                </div>

                <div className="glass-panel" style={{ padding: '2rem', minHeight: '400px', display: 'flex', flexDirection: 'column' }}>
                    <h3 style={{ marginBottom: '2rem' }}>Expenses by Category</h3>
                    {breakdown.length === 0 ? (
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 1, color: 'var(--text-secondary)' }}>
                            No categorized expenses
                        </div>
                    ) : (
                        <div style={{ display: 'flex', flex: 1, gap: '2rem', minHeight: 0 }}>
                            {/* Chart Area */}
                            <div style={{ flex: 1, minWidth: '250px' }}>
                                <ResponsiveContainer width="100%" height="100%">
                                    <PieChart>
                                        <Pie
                                            data={breakdown}
                                            cx="50%"
                                            cy="50%"
                                            innerRadius={60}
                                            outerRadius={80}
                                            fill="#8884d8"
                                            paddingAngle={5}
                                            dataKey="value"
                                        >
                                            {breakdown.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                            ))}
                                        </Pie>
                                        <Tooltip formatter={(value) => `€${value.toFixed(2)}`} />
                                    </PieChart>
                                </ResponsiveContainer>
                            </div>

                            {/* Legend/List Area */}
                            <div style={{ flex: 1, overflowY: 'auto', maxHeight: '300px', paddingRight: '0.5rem' }}>
                                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
                                    <tbody>
                                        {breakdown.map((entry, index) => (
                                            <tr key={index} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                                <td style={{ padding: '0.5rem 0', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                                    <div style={{ width: '12px', height: '12px', borderRadius: '2px', backgroundColor: COLORS[index % COLORS.length] }}></div>
                                                    {entry.name}
                                                </td>
                                                <td style={{ padding: '0.5rem 0', textAlign: 'right', fontWeight: 500 }}>
                                                    €{entry.value.toFixed(2)}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default Dashboard
