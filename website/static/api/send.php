<?php
// Form endpoint for walakelmeh.com: emails each suggestion or partner request to the team.
// Called by the website forms (see SUGGEST_JS in website/build.py). Replies with JSON.

const TO = 'hello@walakelmeh.com';
const FROM = 'no-reply@walakelmeh.com';
const SITE_HOSTS = ['walakelmeh.com', 'www.walakelmeh.com'];
const MAX_PER_WINDOW = 5;      // submissions per visitor
const WINDOW_SECONDS = 600;    // every 10 minutes

// Field => max length. Anything else is ignored.
const FIELDS = [
  'kind' => 20, 'lang' => 5, 'page' => 200, 'name' => 60,
  'category' => 60, 'word' => 80, 'arabizi' => 80, 'level' => 20,
  'category_name' => 60, 'examples' => 400,
  'venue' => 80, 'city' => 40, 'type' => 40, 'contact' => 80, 'message' => 800,
];
const KINDS = ['card' => 'اقتراح بطاقة', 'category' => 'اقتراح فئة', 'partner' => 'طلب شراكة'];

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

function reply(int $code, bool $ok, string $error = ''): void {
  http_response_code($code);
  echo json_encode($ok ? ['success' => true] : ['success' => false, 'error' => $error]);
  exit;
}

function clean(string $v, int $max): string {
  $v = str_replace(["\r\n", "\r"], "\n", trim($v));
  $v = preg_replace('/[\x00-\x09\x0B-\x1F\x7F]/u', '', $v) ?? '';
  return mb_substr($v, 0, $max);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') reply(405, false, 'method');

// Only our own pages may post here.
$origin = $_SERVER['HTTP_ORIGIN'] ?? $_SERVER['HTTP_REFERER'] ?? '';
$host = strtolower(parse_url($origin, PHP_URL_HOST) ?: '');
if (!in_array($host, SITE_HOSTS, true)) reply(403, false, 'origin');

// Honeypot: people never see this box, bots tick it. Pretend it worked.
if (!empty($_POST['botcheck'])) reply(200, true);

// Rate limit per visitor (hashed IP, so no address is stored).
$dir = sys_get_temp_dir() . '/walakelmeh-forms';
if (!is_dir($dir)) @mkdir($dir, 0700, true);
$file = $dir . '/' . hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . __FILE__);
$now = time();
$hits = array_filter(array_map('intval', @file($file, FILE_IGNORE_NEW_LINES) ?: []), fn($t) => $t > $now - WINDOW_SECONDS);
if (count($hits) >= MAX_PER_WINDOW) reply(429, false, 'rate');
$hits[] = $now;
@file_put_contents($file, implode("\n", $hits), LOCK_EX);

$data = [];
foreach (FIELDS as $key => $max) {
  if (isset($_POST[$key]) && is_string($_POST[$key])) {
    $v = clean($_POST[$key], $max);
    if ($v !== '') $data[$key] = $v;
  }
}
$kind = $data['kind'] ?? '';
if (!isset(KINDS[$kind])) reply(400, false, 'kind');
$needed = ['card' => ['word'], 'category' => ['category_name'], 'partner' => ['venue', 'contact']][$kind];
foreach ($needed as $key) if (empty($data[$key])) reply(400, false, 'missing');

$about = $data['word'] ?? $data['category_name'] ?? $data['venue'] ?? '';
$subject = 'ولا كلمة · ' . KINDS[$kind] . ($about !== '' ? ': ' . $about : '');
$body = '';
foreach ($data as $key => $v) $body .= $key . ': ' . $v . "\n";
$body .= "\nSent " . gmdate('Y-m-d H:i') . " UTC from the website.\n";

$headers = [
  'From: =?UTF-8?B?' . base64_encode('موقع ولا كلمة') . '?= <' . FROM . '>',
  'MIME-Version: 1.0',
  'Content-Type: text/plain; charset=UTF-8',
  'Content-Transfer-Encoding: 8bit',
];
// Partners can be answered directly when they left an email.
if (filter_var($data['contact'] ?? '', FILTER_VALIDATE_EMAIL)) $headers[] = 'Reply-To: ' . $data['contact'];

$sent = mail(TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers), '-f' . FROM);
reply($sent ? 200 : 500, $sent, $sent ? '' : 'mail');
