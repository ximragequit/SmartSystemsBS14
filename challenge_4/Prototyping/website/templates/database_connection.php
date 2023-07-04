<!DOCTYPE html>
<html>
<head>
    <title>PostgreSQL-Abfrage mit PHP</title>
</head>
<body>
<h1>Test</h1>
<?php
error_reporting(-1);
ini_set('display_errors','On');
$host = '127.0.0.1';
$dbname = 'ferry';
$user = 'admin_hs';
$password = 'Testing1234';

$dsn = "pgsql:host=$host;dbname=$dbname;user=$user;password=$password";
$pdo = new PDO($dsn);
// SQL-Abfrage ausführen
$sql = 'SELECT * FROM vent_stat';
$stmt = $pdo->query($sql);

// Ergebnisse ausgeben
echo '<table>';
echo '<tr><th>ID</th><th>Name</th><th>Status</th><th>Zeit</th></tr>';
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        echo '<tr>';
        echo '<td>' . $row['vent_stat_id'] . '</td>';
        echo '<td>' . $row['vent_id'] . '</td>';
        echo '<td>' . $row['vent_status'] . '</td>';
        echo '<td>' . $row['zeit'] . '</td>';
        echo '</tr>';
}
echo '</table>';

// Verbindung schließen
$pdo = null;
?>
</body>
</html>