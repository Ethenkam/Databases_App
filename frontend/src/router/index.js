import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import Employees from '../views/Employees.vue'
import Departments from '../views/Departments.vue'
import Documents from '../views/Documents.vue'
import Budget from '../views/Budget.vue'
import Contractors from '../views/Contractors.vue'
import Positions from '../views/Positions.vue'
import Olap from '../views/Olap.vue'

const routes = [
  {
    path: '/',
    component: AppLayout,
    children: [
      { path: '', component: Dashboard },
      { path: 'employees', component: Employees },
      { path: 'departments', component: Departments },
      { path: 'documents', component: Documents },
      { path: 'budget', component: Budget },
      { path: 'contractors', component: Contractors },
      { path: 'positions', component: Positions },
      { path: 'olap', component: Olap },
    ],
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
