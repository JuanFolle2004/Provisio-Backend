<?php

declare(strict_types=1);

namespace Src\Assignment\App\Controllers;

use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Http\JsonResponse;
use Src\Assignment\App\Request\AssignProductRequest;
use Src\Assignment\App\Resources\AssignmentResource;
use Src\Assignment\Domain\Model\Assignment;
use Src\Users\Domain\Models\User;

class AssignProductController
{
    public function __invoke(AssignProductRequest $assignProductRequest, #[CurrentUser] User $currentUser): JsonResponse
    {
        $dto = $assignProductRequest->toDto();
        $assignment = Assignment::create([
            'user_id' => $currentUser->id,
            'product_id' => $dto->productId,
            'group_id' => $dto->groupId,
            'bought' => $dto->bought,
            'amount' => $dto->amount,
        ]);

        return AssignmentResource::make($assignment)->response();
    }
}
