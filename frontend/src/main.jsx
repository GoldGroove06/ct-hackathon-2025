import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Navbar from './components/Navbar.jsx'
import Sidebar from './components/Sidebar.jsx'


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Navbar/>
    <div className='flex flex-row bg-gray-200  w-full'>
      <Sidebar/>
      <div className='mx-auto max-w-7xl'>
<App />
      </div>
   
    </div>
         
  </StrictMode>,
)
