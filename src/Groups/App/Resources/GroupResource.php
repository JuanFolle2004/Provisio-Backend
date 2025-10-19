<?php

declare(strict_types=1);

namespace Src\Groups\App\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Src\Groups\Domain\Model\Group;

/**
 * @mixin Group
 */
class GroupResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'assignments_count' => $this->assignments_count,
            'products_count' => $this->products_count,
            'users_count' => $this->users_count,
        ];
    }
}
