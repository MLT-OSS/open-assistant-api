const routes = [
    {
        path: '/login',
        name: '登录',
        layout: false,
        component: 'login',
        hideInMenu: true
    },
    {
        path: '/playground',
        name: 'Playground',
        component: 'playground',
        icon: 'code'
    },
    {
      path: '/assistants',
      name: 'Assistants',
      component: 'assistants',
      icon: 'areaChart'
    },
    {
      path: '/actions',
      name: 'Actions',
      component: 'actions',
      icon: 'tool'
    },
    { path: '/', redirect: '/playground' },
    { component: './404' }
];
export default routes;
