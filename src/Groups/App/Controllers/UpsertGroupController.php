<?php

declare(strict_types=1);

namespace Src\Groups\App\Controllers;

use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Http\JsonResponse;
use Src\Groups\App\Requests\UpsertGroupRequest;
use Src\Groups\App\Resources\ProductResource;
use Src\Groups\Domain\Model\Group;
use Src\Users\Domain\Models\User;

class UpsertGroupController
{
    public function __invoke(UpsertGroupRequest $request, #[CurrentUser] User $currentUser): JsonResponse
    {
        $dto = $request->toDto();
        $group = Group::create([
            'name' => $dto->name,
            'due_date' => $dto->dueDate->format('Y-m-d'),
        ]);
        $group->users()->attach($currentUser->id);

        return ProductResource::make($group)->response();
    }
}
