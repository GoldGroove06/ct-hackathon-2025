import { useState } from "react"
import { Toast } from "./components/Toast"

const FileIcon = () => (<svg width="50" height="50" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3.5 2C3.22386 2 3 2.22386 3 2.5V12.5C3 12.7761 3.22386 13 3.5 13H11.5C11.7761 13 12 12.7761 12 12.5V6H8.5C8.22386 6 8 5.77614 8 5.5V2H3.5ZM9 2.70711L11.2929 5H9V2.70711ZM2 2.5C2 1.67157 2.67157 1 3.5 1H8.5C8.63261 1 8.75979 1.05268 8.85355 1.14645L12.8536 5.14645C12.9473 5.24021 13 5.36739 13 5.5V12.5C13 13.3284 12.3284 14 11.5 14H3.5C2.67157 14 2 13.3284 2 12.5V2.5Z" fill="currentColor" fill-rule="evenodd" clip-rule="evenodd"></path></svg>)
function App() {
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState(null)
  const [output, setOutput] = useState(null)
  const [loading, setLoading] = useState(false)
  const [toasts, setToasts] = useState([]);

  const showToast = (msg) => {
    const id = Date.now();
    const newToast = (
      <Toast
        key={id}
        message={msg}
        duration={3000}
        onClose={() => setToasts((prev) => prev.filter((t) => t.key !== id))}
      />
    );
    setToasts((prev) => [...prev, newToast]);
  };

  const handleUpload = async () => {
    if (!file) {
      showToast(<div>Please select a file</div>)
      return
    }
    setLoading(true)

    const formData = new FormData();
    formData.append("video", file);

    const res = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    console.log(data)
    setOutput(data.url);
    setLoading(false);
  }
  return (
    <div className="bg-white text-black w-full h-screen flex flex-col  items-center my-8">
      {toasts.map((toast) => toast)}
      <div className="bg-gray-200 rounded-xl w-[400px] h-[200px] flex items-center justify-center mb-8 flex-col flex">
        {loading ? "loading" : (<>
          <FileIcon />
          <input type="file" accept="video/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
          <button onClick={handleUpload} className="bg-teal-500 hover:bg-teal-600 text-white font-bold py-2 px-4 rounded">Upload</button>

        </>)}
      </div>
      {output && (
        <div className="my-8 p-4 bg-gray-200 rounded-3xl">

          <video width="420" height="240" controls className="rounded-2xl">
            <source src={output} type="video/mp4" />
          </video>


        </div>
      )}
    </div>
  )
}

export default App
