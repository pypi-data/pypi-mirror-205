<!DOCTYPE html>
<html>
<head>
    <title>Database Integration</title>
</head>
<body>

    <h1>Tax Portal</h1>

    <?php
    $city = $_POST["city"] ?? "";
    $amount = $_POST["amount"] ?? "";

    $tax = $amount * 0.18;

    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "myDB";

    $conn = mysqli_connect($servername, $username, $password, $dbname);

    $sql = "INSERT INTO orders (city, amount, gst)
    VALUES ('$city', '$amount', '$tax')";

    mysqli_query($conn, $sql);

    mysqli_close($conn);
    ?>

    <form method="post" action="">
        City: <input type="text" name="city"><br><br>
        Total Amount: <input type="text" name="amount"><br><br>
        <input type="submit" name="submit" value="Submit">
    </form>

</body>
</html>
