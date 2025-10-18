<?php

declare(strict_types=1);

namespace Src\Groups\App\Controllers;

use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Http\JsonResponse;
use Src\Groups\App\Requests\AddUserToGroupRequest;
use Src\Groups\App\Resources\GroupResource;
use Src\Groups\Domain\Model\Group;
use Src\Shared\App\Exceptions\Http\UnauthorizedException;
use Src\Users\Domain\Models\User;

class AddUserToGroupController
{
    public function __invoke(
        AddUserToGroupRequest $request,
        Group $group,
        #[CurrentUser]
        User $currentUser,
    ): JsonResponse {
        if (! $group->users->contains($currentUser)) {
            throw new UnauthorizedException('Cant change a group you are not part of');
        }
        $users = $request->toIdArray();

        $group->users()->syncWithoutDetaching($users);

        return GroupResource::make($group)->response();
    }
}
