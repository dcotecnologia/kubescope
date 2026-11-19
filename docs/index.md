---
layout: default
---

<!-- markdownlint-disable MD041 -->
<div class="more">
 <h2>See it at work</h2>
 <figure>
  <img src="{{ '/screenshots/store/deployments-dark.png' | relative_url }}" alt="The Deployments list" loading="lazy">
  <figcaption>The Deployments list, with the Pods, Details and Logs buttons.</figcaption>
 </figure>
 <figure>
  <img src="{{ '/screenshots/store/details-dark.png' | relative_url }}" alt="The JSON of a resource" loading="lazy">
  <figcaption>The JSON of a resource, colored.</figcaption>
 </figure>
 <figure>
  <img src="{{ '/screenshots/store/logs-dark.png' | relative_url }}" alt="Pod logs" loading="lazy">
  <figcaption>Pod logs with colored levels.</figcaption>
 </figure>
</div>
<div class="more">
 <h2>Meet Gabi, your Kubernetes assistant</h2>
 <p>Ask Gabi why a Pod is restarting, what changed in a Deployment, or where to find the evidence. From the round button in the corner, she can inspect the resource, logs and events you need; explain what she found; and take you to the right list, detail or log.</p>
 <ul>
  <li>Paste a screenshot, manifest or long log to add context to the conversation.</li>
  <li>Get an answer in the language of KubeScope, with the checks and evidence behind it.</li>
  <li>Stay safe by default: she cannot change a cluster in read-only mode. With write mode on, every proposed change still waits for your review and <strong>Run</strong>.</li>
 </ul>
 <p>Gabi uses Claude Code or Codex already signed in on your computer; KubeScope asks for no credentials and stores none. <a href="{{ '/assistant/' | relative_url }}" target="_self">Explore Gabi's capabilities and safeguards.</a></p>
</div>
<div class="more">
 <h2>Install it in one command</h2>
 <p>On Linux, <code>curl -fsSL https://raw.githubusercontent.com/dcotecnologia/kubescope/main/install.sh | sh</code>; on Windows, PowerShell has an equivalent. Run it again to update. The <a href="{{ '/install/' | relative_url }}" target="_self">install page</a> has both, and what they do.</p>
</div>
