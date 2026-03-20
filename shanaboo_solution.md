```diff
--- a/deploy/Dockerfile
+++ b/deploy/Dockerfile
@@ -0,0 +1,25 @@
+# Use an official Python runtime as a parent image
+FROM python:3.10-slim
+
+# Set the working directory in the container
+WORKDIR /app
+
+# Copy the current directory contents into the container at /app
+COPY . /app
+
+# Install any needed packages specified in requirements.txt
+RUN pip install --no-cache-dir -r requirements.txt
+
+# Make port 5000 available to the world outside this container
+EXPOSE 5000
+
+# Define environment variable
+ENV NAME World
+
+# Run app.py when the container launches
+CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.app:app"]
+
+--- a/deploy/docker-compose.yml
+++ b/deploy/docker-compose.yml
@@ -1,11 +1,45 @@
-version: '3'
+version: '3.8'
+
+services:
+  web:
+    build: .
+    ports:
+      - "5000:5000"
+    depends_on:
+      - db
+      - redis
+    environment:
+      - DATABASE_URL=postgresql://postgres:password@db:5432/finmind
+      - REDIS_URL=redis://redis:6379/0
+    volumes:
+      - .:/app
+    command: gunicorn -b 0.0.0.0:5000 app.app:app
+
+  db:
+    image: postgres:13
+    environment:
+      POSTGRES_USER: postgres
+      POSTGRES_PASSWORD: password
+      POSTGRES_DB: finmind
+    volumes:
+      - db_data:/var/lib/postgresql/data
+
+  redis:
+    image: redis:6
+    volumes:
+      - redis_data:/data
+
+volumes:
+  db_data:
+  redis_data:
+
+--- a/deploy/kubernetes/deployment.yaml
+++ b/deploy/kubernetes/deployment.yaml
@@ -0,0 +1,45 @@
+apiVersion: apps/v1
+kind: Deployment
+metadata:
+  name: finmind-deployment
+spec:
+  replicas: 3
+  selector:
+    matchLabels:
+      app: finmind
+  template:
+    metadata:
+      labels:
+        app: finmind
+    spec:
+      containers:
+      - name: finmind
+        image: finmind:latest
+        ports:
+        - containerPort: 5000
+        env:
+        - name: DATABASE_URL
+          value: postgres://postgres:password@finmind-db:5432/finmind
+        - name: REDIS_URL
+          value: redis://finmind-redis:6379/0
+        readinessProbe:
+          httpGet:
+            path: /health
+            port: 5000
+          initialDelaySeconds: 5
+          periodSeconds: 10
+        livenessProbe:
+          httpGet:
+            path: /health
+            port: 5000
+          initialDelaySeconds: 15
+          periodSeconds: 20
+
+--- a/deploy/kubernetes/service.yaml
+++ b/deploy/kubernetes/service.yaml
@@ -0,0 +1,12 @@
+apiVersion: v1
+kind: Service
+metadata:
+  name: finmind-service
+spec:
+  selector:
+    app: finmind
+  ports:
+    - protocol: TCP
+      port: 80
+      targetPort: 5000
+  type: LoadBalancer
+
+--- a/deploy/kubernetes/ingress.yaml
+++ b/deploy/kubernetes/ingress.yaml
@@ -0,0 +1,16 @@
+apiVersion: networking.k8s.io/v1
+kind: Ingress
+metadata:
+  name: finmind-ingress
+  annotations:
+    nginx.ingress.kubernetes.io/rewrite-target: /
+spec:
+  rules:
+  - host: finmind.example.com
+    http:
+      paths:
+      - path: /
+        pathType: Prefix
+        backend:
+          service:
+            name: finmind-service
+            port:
+              number: 80
+
+--- a/deploy/kubernetes/hpa.yaml
+++ b/deploy/kubernetes/hpa.yaml
@@ -0,0 +1,12 @@
+apiVersion: autoscaling/v2
+kind: HorizontalPodAutoscaler
+metadata:
+  name: finmind-hpa
+spec:
+  scaleTargetRef:
+    apiVersion: apps/v1
+    kind: Deployment
+    name: finmind-deployment
+  minReplicas: 1
+  maxReplicas: 10
+  metrics:
+  - type: Resource
+    resource:
+      name: cpu
+      target:
+        type: Utilization
+        averageUtilization: 50
+
+--- a/deploy/kubernetes/secret.yaml
+++ b/deploy/kubernetes/secret.yaml
@@ -0,0 +1,10 @@
+apiVersion: v1
+kind: Secret
+metadata:
+  name: finmind-secrets
+type: Opaque
+data:
+  DATABASE_URL: cG9zdGdyZXM6Ly9wb3N0Z3JlcyBwYXNzd29yZEBmaW5taW5kLWRiOjU0MzIvZmlubWluZA==
+  REDIS_URL: cmVkaXM6Ly9maW5taW5kLXJlZGlzOjYzNzkvMA==
+
+--- a/deploy/tilt/Tiltfile
+++ b/deploy/tilt/Tiltfile
@@ -0,0 +1,12 @@
+k8s_yaml([
+    'kubernetes/deployment.yaml',
+    'kubernetes/service.yaml',
+    'kubernetes/ingress.yaml',
+    'kubernetes/hpa.yaml',
+    'kubernetes/secret.yaml'
+])
+
+docker_build('finmind:latest', '.', live_update=[
+    sync('.', '/app'),
+    run('pip install -r requirements.txt')
+])
+
+--- a/deploy/tilt/README.md
+++ b/deploy/tilt/README.md
@@ -0,0 +1,10 @@
+# Tilt Setup for FinMind
+
+To use Tilt for local Kubernetes development, follow these steps:
+
+1.