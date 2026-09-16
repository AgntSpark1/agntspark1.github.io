# Privacy Policy

**Effective date:** September 17, 2026

This policy explains how AgntSpark LLC ("AgntSpark", "we") handles personal
data when you use the AgntSpark website, console, API, SDK, command-line tool
and hosted agents (the "Service").

It covers two roles:

- **Your account data**, which we decide how to use. We are the controller.
- **Data passing through your Agents**, which you decide how to use. We
  process it on your behalf.

## 1. What we collect

**Account data**

- Name and email address.
- Your password, stored only as a bcrypt hash.
- Your role, plan, the invite code you used, and when the account was
  created.

**Billing data**

- If you subscribe to a paid plan, Stripe collects your payment details. We
  receive and store only your Stripe customer ID, subscription ID and
  subscription status. We never see or store full card numbers.

**Keys and configuration**

- API keys and agent access keys, stored only as SHA-256 hashes plus a short
  prefix so you can recognize them.
- Agent configuration: names, models, prompts, container images, resource
  settings and environment variables. Values you mark secret, including
  model provider keys, are encrypted at rest and decrypted only when an
  Agent's container starts.

**Usage and technical data**

- Per agent, per hour: running replicas, reserved CPU and memory, and the
  number of requests routed to the agent. We use these for quotas and
  billing.
- To rate limit requests to Agents, we use the caller's IP address in memory
  for up to one minute. It isn't written to our database.
- Our servers keep operational logs, such as requests to the API, which can
  include IP addresses. They rotate automatically and are overwritten as new
  entries arrive.

**Data passing through your Agents**

- Requests to your Agents and their responses go from our edge proxy
  directly to your Agent's container. We don't store request or response
  bodies.
- Your Agents' console output (logs) is kept on the host while the Agent's
  containers exist, and shown to you in the console.
- What your Agent does with data, and which third parties it sends data to,
  such as your chosen model provider, is up to you.

**Emails you send us**

- Messages you send to our addresses, and the contact details in them.

**Cookies and similar technologies**

- The console keeps your sign-in session token in your browser's local
  storage. We don't use advertising or analytics cookies.

## 2. How we use it

- To provide the Service: authenticate you, run and route your Agents, and
  enforce plan limits and rate limits.
- To bill paid plans.
- To secure the Service, prevent abuse and investigate misuse.
- To contact you about your account, security, and changes to the Service or
  our policies.
- To comply with legal obligations.

We don't sell personal data, and we don't use Your Content to train models.

If you are in the European Economic Area or the United Kingdom, we rely on
these legal bases: performance of our contract with you (providing the
Service and billing), our legitimate interests (securing the Service,
preventing abuse and improving it), compliance with legal obligations, and
your consent where the law requires it.

## 3. Who we share it with

We share personal data only with service providers that help us run the
Service, under terms that limit their use of it:

| Provider | Purpose | Data |
|---|---|---|
| Google Cloud | Hosting the platform (servers and disks) | All data stored by the Service |
| Cloudflare | DNS, hosting of agntspark.com, and routing of email sent to our addresses | Website request metadata; emails you send us |
| Stripe | Payment processing | Billing data |
| Certificate authorities (such as Let's Encrypt) | TLS certificates | Hostnames of agents; certificates are published in public certificate transparency logs |
| Google Fonts | Fonts on agntspark.com | Your IP address and browser details when the page loads fonts |

We may also disclose data if required by law, to protect the rights, safety
or property of AgntSpark, our users or others, or in connection with a
merger, acquisition or sale of assets.

## 4. Where it's stored

The platform runs on Google Cloud servers in Taiwan (region asia-east1). Our
service providers may process data in other countries, including the United
States. Where the law requires a mechanism for international transfers, we
take the steps it requires, such as relying on the European Commission's
Standard Contractual Clauses.

## 5. How long we keep it

- Account, configuration and key data: while your account exists, then
  deleted within 30 days of account deletion.
- Hourly usage records and billing data: as long as needed for billing, tax
  and accounting obligations, generally up to 7 years for paid accounts.
- Database backups: 14 days, after which they are deleted automatically.
- Rate-limit data: about one minute, in memory only.
- Operational logs: overwritten as they rotate.

## 6. Security

Passwords, API keys and access keys are hashed; secret configuration values
are encrypted at rest; traffic is encrypted in transit with TLS; Agents run
in isolated containers with restricted privileges and network access; and
access to production systems is limited. No method of transmission or
storage is completely secure.

## 7. Your rights

Depending on where you live, you may have the right to access, correct,
delete or export your personal data, to object to or restrict certain
processing, and to complain to a data protection authority. To exercise
these rights, email admin@agntspark.com. We will respond within the time the
law requires.

If your Agents process personal data of other people, requests from those
people should go to you; we will help as reasonably required.

## 8. Children

The Service is not for children. We don't knowingly collect personal data
from anyone under 16.

## 9. Changes

We will post changes to this policy here and, for material changes, notify
you by email or in the console before they take effect.

## 10. Contact

AgntSpark LLC
30 N Gould St Ste N, Sheridan, WY 82801, USA
admin@agntspark.com
