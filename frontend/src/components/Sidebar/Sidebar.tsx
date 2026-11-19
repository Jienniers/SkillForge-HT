import { NavLink } from 'react-router'

function Sidebar() {
  const menuItems = [
    { name: 'Dashboard', path: '/' },
    { name: 'Analytics', path: '/analytics' },
  ]

  return (
    <aside className="w-64 min-h-screen bg-slate-900 text-white p-5">

      <h1 className="text-xl font-bold mb-8">
        MyApp
      </h1>

      <nav className="space-y-2">

        {menuItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) =>
              `block p-3 rounded-lg ${
                isActive
                  ? 'bg-blue-600'
                  : 'hover:bg-slate-800'
              }`
            }
          >
            {item.name}
          </NavLink>
        ))}

      </nav>
    </aside>
  )
}

export default Sidebar