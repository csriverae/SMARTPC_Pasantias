export const ErrorMessage = ({ message }) => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      <p>{message}</p>
    </div>
  </div>
)