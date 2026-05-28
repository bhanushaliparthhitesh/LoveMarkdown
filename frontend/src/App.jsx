import { useMemo, useState } from 'react'
import ReactMarkdown from 'react-markdown'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function App() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)

  const canConvert = useMemo(() => !!file && !loading, [file, loading])

  const onDrop = (event) => {
    event.preventDefault()
    setFile(event.dataTransfer.files?.[0] || null)
  }

  const onConvert = async () => {
    if (!file) return
    setError('')
    setLoading(true)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${API_URL}/api/convert`, {
        method: 'POST',
        body: formData
      })
      if (!response.ok) {
        const payload = await response.json()
        throw new Error(payload.detail || 'Conversion failed')
      }
      setResult(await response.json())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const onExport = async () => {
    if (!result) return
    const response = await fetch(`${API_URL}/api/export`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(result)
    })

    const markdown = await response.text()
    const blob = new Blob([markdown], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${result.filename.replace(/\.[^.]+$/, '')}.md`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <main className="container">
      <h1>LovePrompt</h1>
      <p>Convert documents into AI-ready Markdown for LLM workflows.</p>

      <label className="dropzone">
        <input
          type="file"
          onChange={(event) => setFile(event.target.files?.[0] || null)}
          hidden
        />
        <div
          onDragOver={(event) => event.preventDefault()}
          onDrop={onDrop}
        >
          {file ? `Selected: ${file.name}` : 'Drag/drop or click to upload PDF, DOCX, PPTX, TXT...'}
        </div>
      </label>

      <div className="actions">
        <button disabled={!canConvert} onClick={onConvert}>
          {loading ? 'Converting...' : 'Convert'}
        </button>
        <button disabled={!result} onClick={onExport}>Export Markdown</button>
      </div>

      {error && <p className="error">{error}</p>}

      {result && (
        <section className="result">
          <div className="meta">
            <strong>Estimated tokens:</strong> {result.estimated_tokens}
          </div>
          <h2>Optimized Markdown Preview</h2>
          <article className="preview">
            <ReactMarkdown>{result.optimized_markdown}</ReactMarkdown>
          </article>
        </section>
      )}
    </main>
  )
}
