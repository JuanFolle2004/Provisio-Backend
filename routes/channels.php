<?php

use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Support\Facades\Broadcast;
use Src\Users\Domain\Models\User;
use Illuminate\Support\Facades\Log;

Broadcast::channel('App.Models.User.{id}', function ($user, $id) {
    return (int) $user->id === (int) $id;
});

Broadcast::channel('chat.group.{id}', function (User $user, int $id) {
    Log::info("User {$user->id} tried to join chat for group {$id}");
    return $user->groups->pluck('id')->contains($id);
},['guard'=>'api']);
