<?php

declare(strict_types=1);

namespace Src\Groups\App\Controllers;

use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Http\JsonResponse;
use Src\Groups\App\Resources\GroupResource;
use Src\Groups\App\Resources\ProductResource;
use Src\Users\Domain\Models\User;

class ListGroupsController
{
    public function __invoke(
        #[CurrentUser]
        User $currentUser,
    ): JsonResponse {
        return GroupResource::collection($currentUser->groups()->with(['users','assignments','products'])->get())->response();
    }
}
