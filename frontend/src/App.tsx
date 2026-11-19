import { BrowserRouter, Routes, Route } from 'react-router'

import Sidebar from './components/Sidebar/Sidebar'

import Dashboard from './pages/Dashboard'
import Analytics from './pages/Analytics'

function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-slate-950 text-white">

        <Sidebar />

        <main className="flex-1 p-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </main>

      </div>
    </BrowserRouter>
  )
}

export default App