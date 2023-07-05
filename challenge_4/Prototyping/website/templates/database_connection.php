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

function psql($sqlQuery, $echo1) {
        $host = '127.0.0.1';
        $dbname = 'ferry';
        $user = 'admin_hs';
        $password = 'Testing1234';
        $pdo = new PDO("pgsql:host=$host;dbname=$dbname", $user, $password);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $stmt = $pdo->prepare($sqlQuery);
        $stmt->execute();
        $information = $stmt->fetchColumn();
        if ($echo1 == 1) {
                echo $information;
        }
        return $information; // Gib den Wert zurück
}

psql("SELECT dockname FROM dock where dock_id = 2;", 1);
?>
<p>Der Captain John Smith
<?php
$availability = psql("SELECT availability FROM captain where captain_id = 1;", 0);
echo $availability;
if ($availability == true) {
        echo "ist abwesend";
} else {
        echo "ist anwesend";
}
?></p>

</body>
</html>