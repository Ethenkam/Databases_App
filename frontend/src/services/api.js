import axios from 'axios'

const http = axios.create({ baseURL: 'http://localhost:8000/api' })

export const api = {
  getAll(endpoint, page = 1, size = 20) {
    return http.get(`/${endpoint}`, { params: { page, size } }).then(r => r.data)
  },

  getOne(endpoint, id) {
    return http.get(`/${endpoint}/${id}`).then(r => r.data)
  },

  create(endpoint, data) {
    return http.post(`/${endpoint}`, data).then(r => r.data)
  },

  update(endpoint, id, data) {
    return http.put(`/${endpoint}/${id}`, data).then(r => r.data)
  },

  delete(endpoint, id) {
    return http.delete(`/${endpoint}/${id}`)
  },

  olap: {
    rollupByDept: () =>
      http.get('/olap/rollup-by-dept').then(r => r.data),
    rollupByItem: () =>
      http.get('/olap/rollup-by-item').then(r => r.data),
    rollupByQuarter: () =>
      http.get('/olap/rollup-by-quarter').then(r => r.data),
    crossDeptItem: () =>
      http.get('/olap/cross-dept-item').then(r => r.data),
    drilldownDept: (deptId) =>
      http.get('/olap/drilldown-dept', { params: { dept_id: deptId } }).then(r => r.data),
    sliceByDept: (deptId) =>
      http.get('/olap/slice-by-dept', { params: { dept_id: deptId } }).then(r => r.data),
    sliceByContractor: (contrInn) =>
      http.get('/olap/slice-by-contractor', { params: { contr_inn: contrInn } }).then(r => r.data),
    dice: (params) =>
      http.get('/olap/dice', { params }).then(r => r.data),
  },
}
