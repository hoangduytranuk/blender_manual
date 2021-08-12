I don't know much about PHP but looking around, I found this way to complete this task:

<?php
    $data = [
        array(
            'title' => 'Call of duty',
            'type' => 'Shooter',
            'price' => 59.95
        ),
        array(
            'title' => 'Rocket League',
            'type' => 'Sport',
            'price' => 49.95
        ),
        array(
            'title' => 'Assasins Creed',
            'type' => 'RP',
            'price' => 19.95
        )
    ];
    $sum = array_sum($data, 'price');
    $count = count($data);
    $avg = $sum / $count;
?>

I think there should be a more structured way to organise data into records for easier access to 'price'


