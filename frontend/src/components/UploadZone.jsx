import { useState } from 'react'
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react'

const UploadZone = ({ onUploadComplete }) => {
    const [isDragging, setIsDragging] = useState(false)
    const [isUploading, setIsUploading] = useState(false)
    const [error, setError] = useState(null)
    const [success, setSuccess] = useState(null)

    const handleDrag = (e) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setIsDragging(true)
        } else if (e.type === 'dragleave') {
            setIsDragging(false)
        }
    }

    const handleDrop = (e) => {
        e.preventDefault()
        e.stopPropagation()
        setIsDragging(false)
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleUpload(e.dataTransfer.files)
        }
    }

    const handleChange = (e) => {
        e.preventDefault()
        if (e.target.files && e.target.files.length > 0) {
            handleUpload(e.target.files)
        }
    }

    const handleUpload = async (files) => {
        if (!files || files.length === 0) return

        setIsUploading(true)
        setError(null)
        setSuccess(null)

        const formData = new FormData()
        // Append each file with the key 'files' as expected by FastAPI List[UploadFile]
        Array.from(files).forEach(file => {
            formData.append('files', file)
        })

        try {
            const response = await fetch('http://localhost:8000/upload', {
                method: 'POST',
                body: formData,
            })

            if (!response.ok) {
                const errData = await response.json()
                throw new Error(errData.detail || 'Upload failed')
            }

            const data = await response.json()
            // Create summary string
            const successCount = data.details.filter(r => r.status === 'success').length
            const errorCount = data.details.filter(r => r.status === 'error').length

            let msg = `Processed ${successCount} files successfully.`
            if (errorCount > 0) msg += ` ${errorCount} failed.`

            setSuccess(msg)
            setTimeout(() => {
                onUploadComplete()
            }, 2000)
        } catch (err) {
            setError(err.message)
        } finally {
            setIsUploading(false)
        }
    }

    return (
        <div
            className={`glass-panel ${isDragging ? 'dragging' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            style={{
                padding: '3rem',
                textAlign: 'center',
                border: isDragging ? '2px dashed var(--accent-primary)' : '2px dashed rgba(255,255,255,0.1)',
                transition: 'all 0.2s'
            }}
        >
            <input
                type="file"
                id="file-upload"
                accept=".pdf"
                multiple
                onChange={handleChange}
                style={{ display: 'none' }}
            />

            {!isUploading && !success && !error && (
                <label htmlFor="file-upload" style={{ cursor: 'pointer', display: 'block' }}>
                    <div style={{ marginBottom: '1rem' }}>
                        <Upload size={48} color="var(--accent-primary)" />
                    </div>
                    <h3 style={{ marginBottom: '0.5rem' }}>Click or Drag PDF(s) here</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>Upload one or multiple statements</p>
                </label>
            )}

            {isUploading && (
                <div className="animate-fade-in">
                    <FileText size={48} className="animate-pulse" color="var(--accent-secondary)" />
                    <p style={{ marginTop: '1rem' }}>Analyzing transactions...</p>
                </div>
            )}

            {success && (
                <div className="animate-fade-in">
                    <CheckCircle size={48} color="var(--success)" />
                    <p style={{ marginTop: '1rem', color: 'var(--success)' }}>{success}</p>
                </div>
            )}

            {error && (
                <div className="animate-fade-in">
                    <AlertCircle size={48} color="var(--danger)" />
                    <p style={{ marginTop: '1rem', color: 'var(--danger)' }}>{error}</p>
                    <button className="btn btn-outline" onClick={() => setError(null)} style={{ marginTop: '1rem' }}>Try Again</button>
                </div>
            )}
        </div>
    )
}

export default UploadZone
