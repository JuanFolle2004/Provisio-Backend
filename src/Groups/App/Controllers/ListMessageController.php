<?php

declare(strict_types=1);
namespace Src\Groups\App\Controllers;

use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Http\JsonResponse;
use Src\Groups\App\Resources\MessageResource;
use Src\Groups\Domain\Model\Group;
use Src\Groups\Domain\Model\Thread;

class ListMessageController
{
    public function __invoke(#[CurrentUser] $user, Group $group): JsonResponse
    {
        $thread = $group->thread;
        if (! $thread) {
            $thread = new Thread();
            $group->thread()->save($thread);
        }
        $messages = $thread->messages;
        $messages->load('user');

        return MessageResource::collection($messages)->response();
    }
}
