# 如何使用;
`FallbackComponent`: 自定义降级组件

在需要监控ErrorBoundary的组件或者layout中，加入ErrorBoundary
```
<ErrorBoundary FallbackComponent={CustomerError}>{props.children}</ErrorBoundary>
```