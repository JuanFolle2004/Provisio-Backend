<?php

declare(strict_types=1);

namespace Src\Assignment\App\Controllers;

use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Http\JsonResponse;
use Src\Assignment\App\Resources\AssignmentResource;
use Src\Users\Domain\Models\User;

class ListAssignmentsController
{
    public function __invoke(#[CurrentUser] User $currentUser): JsonResponse
    {
        $assignments = $currentUser->assignments()->with(['user', 'product'])->whereRelation(
            'group',
            'due_date',
            '>=',
            now()
        )->get();

        return AssignmentResource::collection($assignments)->response();
    }
}
